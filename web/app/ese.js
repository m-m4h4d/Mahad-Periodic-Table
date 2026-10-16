// Browser port of project/ESE.py.
//
// Each function mirrors its Python counterpart (same names, coordinates,
// fonts and colours) so the web version looks and behaves like the desktop
// app. Text files are kept in the browser's localStorage instead of on disk.

import {
  Tk, Canvas, Label, Button, Entry, Listbox, Scrollbar, StringVar,
  messagebox as tmsg, partial, fitStage, END, RIDGE, GROOVE,
} from './tk.js';
import { IMAGE_FILES, GALLERY_ELEMENTS, QUIZ_ELEMENTS, TABLE_TEXT } from './data.js';

const ASSETS = 'assets/';

// ---------------------------------------------------------------- files

// Minimal stand-in for open(): the two writable files live in localStorage
// (seeded from the copies shipped with the project), Periodictable.txt is
// read-only.
const files = {};
const WRITABLE = ['students_account.txt', 'user_element_info.txt'];
const storageKey = (name) => `mahad-periodic-table:${name}`;

function storageGet(name) {
  try { return localStorage.getItem(storageKey(name)); } catch { return null; }
}

function storageSet(name, text) {
  try { localStorage.setItem(storageKey(name), text); } catch { /* keep it in memory only */ }
}

async function loadFiles() {
  const names = ['Periodictable.txt', ...WRITABLE];
  await Promise.all(names.map(async (name) => {
    const saved = WRITABLE.includes(name) ? storageGet(name) : null;
    if (saved !== null) {
      files[name] = saved;
      return;
    }
    const res = await fetch(ASSETS + name);
    files[name] = res.ok ? (await res.text()).replace(/\r\n?/g, '\n') : '';
  }));
}

function open(name, mode = 'r') {
  if (mode === 'a') {
    return {
      write(s) { files[name] = (files[name] || '') + s; storageSet(name, files[name]); },
      writelines(list) { this.write(list.join('')); },
      close() {},
    };
  }
  throw new Error(`open(${name}, ${mode}) is not supported`);
}

function READ_LINES(name) {
  return (files[name] || '').match(/[^\n]*\n|[^\n]+$/g) || [];
}

// Python string helpers
const strip = (s) => s.trim();
const isnumeric = (s) => /^\p{N}+$/u.test(s);
const len = (s) => [...s].length;
const stripNewlines = (s) => s.replace(/^\n+|\n+$/g, '');
const lower = (s) => s.toLowerCase();

// ---------------------------------------------------------------- globals

let root;
let app_list, cms1_var, element_var;
let user_info_var, user_name_var, ele_name_var, cms_var;
let elements, images, image_index, label, entry_var;
let score, element, ANS_VAR, name_label;
let new_CMS_var, new_pass_var, pre_CMS_var, pre_pass_var;

// STANDARD CMS ID LENGTH IS ELEVEN IN OUR PROJECT SUCH AS 00000000000

// FUNCTION TO REMOVE THE WIDGETS OF THE PREVIOUS SCREEN SO THEY DO NOT PILE UP
// (WIDGETS PLACED HIGHER THAN from_y, LIKE THE TITLE, ARE KEPT)

function CLEAR_SCREEN(from_y = 0) {
  for (const widget of root.winfo_children()) {
    if (parseInt(widget.place_info().y ?? '0', 10) >= from_y) widget.destroy();
  }
}

// FUNCTION TO LOGOUT

async function BACK_TO_MAIN() {
  const ret = await tmsg.askquestion('MAIN PAGE', 'DO YOU WANT TO LOGOUT');
  if (ret === 'yes') main();
  if (ret === 'no') EXECUTION();
}

// FUNCTION FOR DISPLAYING INFORMATION ENTER BY USERS

const detail_list = ['CMS ID:', 'NAME:', 'ELEMENT NAME:', 'INFORMATION:'];

function insertDetails(data) {
  data.slice(0, detail_list.length).forEach((i, index) => app_list.insert(END, `${detail_list[index]} ${i}`));
}

function SEARCH_ALL() {
  app_list.delete(0, END);
  let student_count = 0;
  for (const line of READ_LINES('user_element_info.txt')) {
    if (!strip(line)) continue;
    const data = stripNewlines(line).split('***');
    student_count += 1;
    app_list.insert(END, ' ');
    app_list.insert(END, ` STUDENT : ${student_count} :-`);
    insertDetails(data);
  }
  if (student_count === 0) tmsg.showinfo('Sorry', 'no information added yet!');
}

// FUNCTION FOR SEARCHING INFORMATION ENTER BY USER ON ELEMENT BASIS

function SEARCH_BY_ELEMENT() {
  let flag = 0;
  if (strip(element_var.get()) === '') {
    tmsg.showinfo('Error', 'Invalid Entries!');
    return;
  }
  app_list.delete(0, END);
  let student_count = 0;
  for (const line of READ_LINES('user_element_info.txt')) {
    const data = stripNewlines(line).split('***');
    if (data.length > 2 && lower(strip(data[2])) === lower(strip(element_var.get()))) {
      flag = 1;
      student_count += 1;
      app_list.insert(END, ' ');
      app_list.insert(END, `DATA # : ${student_count} :-`);
      insertDetails(data);
    }
  }
  if (flag === 0) tmsg.showinfo('Sorry', 'element not found!');
}

// FUNCTION FOR SEARCHING INFORMATION ENTER BY USER ON CMS ID BASIS

function DISPLAY_USER_INFO() {
  let flag = 0;
  if (len(strip(cms1_var.get())) !== 11) {
    tmsg.showinfo('Error', 'Invalid Entries ... PLEASE TRY AGAIN !');
    return;
  }
  app_list.delete(0, END);
  let student_count = 0;
  for (const line of READ_LINES('user_element_info.txt')) {
    const data = stripNewlines(line).split('***');
    if (strip(data[0]) === strip(cms1_var.get())) {
      flag = 1;
      student_count += 1;
      app_list.insert(END, ' ');
      app_list.insert(END, `DATA # : ${student_count} :-`);
      insertDetails(data);
    }
  }
  if (flag === 0) tmsg.showinfo('Sorry', 'student not found!');
}

// FUNCTION FOR DISPLAYING LAYOUT OF USER's INFORMATION

function SHOW_BUTTON() {
  CLEAR_SCREEN(180);
  const search_rectangle = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  search_rectangle.place({ x: 0, y: 180 });
  new Label(search_rectangle, { text: 'SEARCH BY CMS ID:', font: ['Segoe UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 20, y: 20 });
  new Label(search_rectangle, { text: 'SEARCH BY ELEMENT:', font: ['Segoe UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 20, y: 200 });
  cms1_var = new StringVar();
  element_var = new StringVar();
  new Entry(search_rectangle, { textvariable: cms1_var, width: 30, font: 20 }).place({ x: 20, y: 70 });
  new Entry(search_rectangle, { textvariable: element_var, width: 30, font: 20 }).place({ x: 20, y: 250 });

  new Button(search_rectangle, { text: 'Search', font: 'SegoeUI 11', command: DISPLAY_USER_INFO }).place({ x: 300, y: 100 });
  new Button(search_rectangle, { text: 'Search', font: 'SegoeUI 11', command: SEARCH_BY_ELEMENT }).place({ x: 300, y: 280 });
  new Button(search_rectangle, { text: 'Search All', font: 'SegoeUI 25', height: 1, width: 10, command: SEARCH_ALL }).place({ x: 100, y: 320 });
  const sby = new Scrollbar(search_rectangle, {});
  app_list = new Listbox(search_rectangle, {
    height: 10, width: 70, font: 'SegoeUI 15', yscrollcommand: sby.set, fg: '#FFFF00', bg: '#4169E1',
  });
  app_list.place({ x: 500, y: 150 });
  sby.config({ command: (...a) => app_list.yview(...a) });
  sby.place({ x: 500 + app_list.winfo_reqwidth(), y: 150, height: app_list.winfo_reqheight() });

  new Button(root, { text: 'BACK', font: 'arial 11', bg: 'LIGHTBLUE', command: USER_INFO }).place({ x: 1300, y: 710 });
}

// FUNCTION FOR WRITING USER INFORMATION IN TEXT FILE

async function WRITING_USER_INFO() {
  const entries = [cms_var, user_name_var, ele_name_var, user_info_var].map((v) => strip(v.get()));
  if (!(isnumeric(entries[0]) && len(entries[0]) === 11)) {
    tmsg.showinfo('Error', 'CMS ID IS INVALID!');
    return;
  }
  if (entries.includes('')) {
    tmsg.showinfo('Error', 'PLEASE FILL IN ALL THE FIELDS!');
    return;
  }
  if (entries.some((entry) => entry.includes('*'))) {
    tmsg.showinfo('Error', 'THE * CHARACTER IS NOT ALLOWED!');
    return;
  }

  open('user_element_info.txt', 'a').write(entries.join('***') + '\n');
  await tmsg.showinfo('information', 'INFORMATION ADDED SUCCESSFULLY');
  user_info_var.set('');
  user_name_var.set('');
  ele_name_var.set('');
  cms_var.set('');
}

// FUNCTON THAT WILL ASK USER TO ENTER INFORMATION IF HE/SHE WANTS

function USER_INFO() {
  CLEAR_SCREEN(180);
  const rectangle_doc = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  rectangle_doc.place({ x: 0, y: 180 });
  new Label(rectangle_doc, { text: 'CMS ID', font: ['Segue UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 350, y: 100 });
  new Label(rectangle_doc, { text: 'NAME', font: ['Segue UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 350, y: 200 });
  new Label(rectangle_doc, { text: 'ELEMENT NAME', font: ['Segue UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 350, y: 300 });
  new Label(rectangle_doc, { text: 'INFORMATION', font: ['Segue UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 350, y: 400 });

  // DISPLAYING BUTTONS FOR INFORMATION ASKED BY USER

  user_info_var = new StringVar();
  user_name_var = new StringVar();
  ele_name_var = new StringVar();
  cms_var = new StringVar();
  new Entry(rectangle_doc, { textvariable: cms_var, width: 30, font: 20 }).place({ x: 750, y: 100 });
  new Entry(rectangle_doc, { textvariable: user_name_var, width: 30, font: 20 }).place({ x: 750, y: 200 });
  new Entry(rectangle_doc, { textvariable: ele_name_var, width: 30, font: 20 }).place({ x: 750, y: 300 });
  new Entry(rectangle_doc, { textvariable: user_info_var, width: 30, font: 20 }).place({ x: 750, y: 400 });
  new Button(rectangle_doc, { text: 'SAVE', font: 'arial 11', bg: 'lightblue', command: WRITING_USER_INFO }).place({ x: 1040, y: 450 });
  new Button(rectangle_doc, { text: 'SHOW INFORMATION', font: 'arial 11', bg: 'lightblue', command: SHOW_BUTTON }).place({ x: 750, y: 450 });

  new Button(rectangle_doc, { text: 'BACK', font: 'arial 11', bg: 'LIGHTBLUE', command: EXECUTION }).place({ x: 1300, y: 550 });
}

// TO SEARCH IMAGE ON THE BASIS OF ITS ATOMIC NUMBER

function update_image() {
  label.configure({ image: images[image_index - 1] });
  if (name_label) name_label.destroy();
  name_label = new Label(root, { text: elements[image_index - 1], width: '15', font: 'SegoeUI 15 bold' });
  name_label.place({ x: 500, y: 679 });
}

// FUNCTION TO GO TO NEXT IMAGE

function NEXT_IMAGE() {
  image_index += 1;
  if (image_index > images.length) image_index = 1;
  update_image();
}

// FUNCTION TO GO TO PREVIOUS IMAGE

function PREV_IMAGE() {
  image_index -= 1;
  if (image_index < 1) image_index = images.length;
  update_image();
}

// FUNCTION UPDATE INDEX OF IMAGE

function UPDATE_INDEX() {
  // int() accepts surrounding whitespace, a sign and underscores between digits
  const text = strip(entry_var.get());
  if (!/^[+-]?\d+(_\d+)*$/.test(text)) {
    tmsg.showerror('Error', 'Invalid Atomic Number');
    return;
  }
  const new_index = parseInt(text.replace(/_/g, ''), 10);
  if (new_index < 1 || new_index > images.length) {
    tmsg.showerror('Error', 'Invalid Atomic Number');
  } else {
    image_index = new_index;
    update_image();
  }
}

// FUNCTION TO PRESENT PICTURES OF ELEMENTS

function PICTURES() {
  CLEAR_SCREEN(180);
  new Label(null, { text: ' ELEMENTAL GALLERY ', font: 'SegueUI 40 bold', bg: '#FFFFF0' }).place({ x: 350, y: 70 });
  const rectangle_doc = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  rectangle_doc.place({ x: 0, y: 180 });

  // LIST OF ELEMENT PICTURES

  const image_files = IMAGE_FILES;

  // LIST OF ELEMENT NAMES

  elements = [...GALLERY_ELEMENTS];

  images = image_files.map((f) => ASSETS + f);
  // PhotoImage loads every picture up front; warm the browser cache likewise.
  images.forEach((src) => { new Image().src = src; });

  image_index = 1;
  name_label = null;

  // DISPLAYING BUTTONS FOR PICTURES TO MOVE FORWARD AND BACKWARD

  label = new Label(root, { image: images[0] });
  label.place({ x: 500, y: 250 });
  new Label(rectangle_doc, { text: elements[image_index - 1], width: '15', height: '1', font: 'SegueUI 15 bold' }).place({ x: 500, y: 500 });
  new Button(rectangle_doc, { text: 'Previous', fg: '#FFFF00', bg: '#4169E1', width: 10, height: 1, command: PREV_IMAGE }).place({ x: 10, y: 400 });
  new Button(rectangle_doc, { text: 'Next', fg: '#FFFF00', bg: '#4169E1', width: 10, height: 1, command: NEXT_IMAGE }).place({ x: 100, y: 400 });

  new Label(rectangle_doc, { text: 'ENTER THE ATOMIC NUMBER ', fg: '#FFFF00', bg: '#4169E1', font: 'SegueUI 15 bold' }).place({ x: 10, y: 40 });
  entry_var = new StringVar();
  new Entry(rectangle_doc, { textvariable: entry_var, width: 30, font: ['aerial', 10] }).place({ x: 10, y: 75 });
  new Button(rectangle_doc, { text: 'Update', fg: '#FFFF00', bg: '#4169E1', width: 10, height: 1, command: UPDATE_INDEX }).place({ x: 10, y: 100 });

  new Button(rectangle_doc, { text: 'BACK', font: 'arial 11', bg: 'LIGHTBLUE', command: EXECUTION }).place({ x: 1300, y: 550 });
}

// TO CHECK ANS ENTER BY USER IS CORRECT OR NOT

async function guess_check() {
  root.title('QUIZ GAME');

  // REMOVE THE RESULT OF THE PREVIOUS ANSWER
  for (const widget of root.winfo_children()) {
    if (widget.quiz_result) widget.destroy();
  }
  const result = (text, y) => {
    const w = new Label(null, { text, font: ['Segue UI', 25], fg: '#FFFF00', bg: '#051047' });
    w.quiz_result = true;
    w.place({ x: 50, y });
  };

  if (strip(ANS_VAR.get()).toLowerCase() === element.toLowerCase()) {
    result('CORRECT ANSWER', 500);
    score += 10;
    delete elements[element];
    if (!Object.keys(elements).length) {
      await tmsg.showinfo('quiz game', `WELL DONE! YOU NAMED ALL THE ELEMENTS\nYOUR SCORE IS ${score}`);
      EXECUTION();
      return;
    }
    quiz();
  } else {
    result('WRONG ANSWER    ', 500);
    result(`YOUR SCORE IS ${score}`, 550);
    const ret = await tmsg.askquestion('quiz game', 'DO YOU WANT TO PLAY AGAIN');
    if (ret === 'yes') QUIZ_GAME();
    if (ret === 'no') EXECUTION();
  }
}

// TO ASK QUIZ TO THE USER

function quiz() {
  root.title('QUIZ GAME');
  const keys = Object.keys(elements);
  element = keys[Math.floor(Math.random() * keys.length)];

  // REMOVE THE PREVIOUS QUESTION
  for (const widget of root.winfo_children()) {
    if (widget.quiz_question) widget.destroy();
  }

  // DISPLAYING INFO FOR QUIZ IN LISTBOX

  const game_listbox = new Listbox(root, { width: 80, height: 5, font: 'calibre 25', bg: 'lightblue' });
  game_listbox.insert(END, `Atomic Number: ${elements[element]['Atomic Number']}`);
  game_listbox.insert(END, `Properties: ${elements[element]['Properties']}`);
  game_listbox.insert(END, `Symbol: ${elements[element]['Symbol']}`);
  game_listbox.insert(END, `Group: ${elements[element]['Group']}`);
  game_listbox.insert(END, `Period: ${elements[element]['Period']}`);
  game_listbox.place({ x: 50, y: 200 });
  const question = [game_listbox];
  question.push(new Label(null, { text: 'ENTER THE ANSWER', font: ['Se-geo UI', 25], fg: '#FFFF00', bg: '#051047' }).place({ x: 50, y: 445 }));
  ANS_VAR = new StringVar();
  question.push(new Entry(null, { textvariable: ANS_VAR, width: 30, font: 20 }).place({ x: 450, y: 450 }));
  question.push(new Button(null, { text: 'CHECK', font: 'arial 11', command: guess_check }).place({ x: 720, y: 500 }));

  question.push(new Button(root, { text: 'BACK', font: 'arial 11', bg: 'LIGHTBLUE', command: EXECUTION }).place({ x: 1300, y: 750 }));
  for (const widget of question) widget.quiz_question = true;
}


// FUNCTION CONTAINING DATA FOR THE QUIZ

function QUIZ_GAME() {
  root.title('QUIZ GAME');
  CLEAR_SCREEN(180);
  const rectangle_doc = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  rectangle_doc.place({ x: 0, y: 180 });

  score = 0;

  // CREATING NESTED DICTIONARY FOR QUIZ

  elements = structuredClone(QUIZ_ELEMENTS);

  quiz();
}

// FUNCTION EXTRACTING INFORMATION FROM TEXT FILE OF ELEMENTS OF PERIODIC TABLE

function txtfile(k) {
  root.title('info');
  CLEAR_SCREEN(180);
  const rectangle_doc = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  rectangle_doc.place({ x: 0, y: 180 });

  const ALL_COLUMNS = ['Atomic Number : ', 'Symbol : ', 'Element : ', 'Origin of name : ',
    'Group : ', 'Period : ', 'Atomic weight : ', 'Density (g/cm^3): ',
    'Melting point (K) : ', 'Boiling point (K): ',
    'Specific heat capacity (J/g . K): ', 'Electronegativity : ',
    "Abundance in earth's crust (mg/kg): "];

  // CREATING LISTBOX FOR DISPLAYING INFORMATION OF ELEMENTS

  const info_listbox = new Listbox(root, { width: 80, height: 13, font: 'calibri 25', bg: 'lightblue' });

  for (const line of READ_LINES('Periodictable.txt')) {
    const data = stripNewlines(line).split('*');
    if (String(k) === strip(data[0])) {
      data.slice(0, ALL_COLUMNS.length).forEach((i, index) => info_listbox.insert(END, `${ALL_COLUMNS[index]} ${i}`));
      break;
    }
  }
  info_listbox.place({ x: 80, y: 200 });

  new Button(null, { text: 'BACK', font: 'arial 11', bg: 'LIGHTBLUE', command: INFO_ELEMENTS }).place({ x: 1300, y: 750 });
}

// FUNCTON PASSING ARGUMENTS  TO ABOVE ONE FOR DISPLAYING INFORMATION OF ELEMENTS

function INFO_ELEMENTS() {
  CLEAR_SCREEN(180);
  const rectangle_doc = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  rectangle_doc.place({ x: 0, y: 180 });
  const blockLabel = (text, x, y) =>
    new Label(rectangle_doc, { text, font: ['Segoe UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x, y });
  blockLabel('f-BLOCK\nELEMENTS', 200, 445);
  blockLabel('p-BLOCK\nELEMENTS', 950, 20);
  blockLabel('d-BLOCK\nELEMENTS', 600, 100);
  blockLabel('s-BLOCK\nELEMENTS', 100, 200);

  // USING A LOOP TO DISPLAY BUTTONS AND PASSING ATOMIC NUMBER AS ARGUMENTS

  const d = 100;
  const elementButton = (text, bg, e, x, y) =>
    new Button(rectangle_doc, {
      text, width: 5, height: 2, font: 'Arial 10 bold', fg: 'black', bg, command: partial(txtfile, e),
    }).place({ x, y });

  // Each column starts at atomic number e and row offset c, then steps down
  // the periods (+2/+8/+8/+18/+18/+32/+32 depending on the row).
  const column = (symbols, e, c, x, bg, step) => {
    for (const sym of symbols) {
      elementButton(sym, bg, e, x, c + 100);
      e += step(e);
      c += 43;
    }
  };

  column(['H', 'Li', 'Na', 'K', 'Rb', 'Cs', 'Fr'], 1, 0, d + 200, 'orange',
    (e) => (e === 1 ? 2 : e === 3 || e === 11 ? 8 : e === 19 || e === 37 ? 18 : 32));
  column(['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra'], 4, 43, d + 250, 'yellow',
    (e) => (e === 4 || e === 12 ? 8 : e === 20 || e === 38 ? 18 : 32));
  column(['Sc', 'Y', 'La', 'Ac'], 21, 129, d + 300, 'light yellow', (e) => (e === 21 || e === 39 ? 18 : 32));

  const dBlock = [
    [['Ti', 'Zr', 'Hf', 'Rf'], 22, 350, 'light yellow'],
    [['V', 'Nb', 'Ta', 'Db'], 23, 400, 'light yellow'],
    [['Cr', 'Mo', 'W', 'Sg'], 24, 450, 'lightyellow'],
    [['Mn', 'Tc', 'Re', 'Bh'], 25, 500, 'light yellow'],
    [['Fe', 'Ru', 'Os', 'Hs'], 26, 550, 'light yellow'],
    [['Co', 'Rh', 'Ir', 'Mt'], 27, 600, 'light yellow'],
    [['Ni', 'Pd', 'Pt', 'Ds'], 28, 650, 'light yellow'],
    [['Cu', 'Ag', 'Au', 'Rg'], 29, 700, 'lightyellow'],
    [['Zn', 'Cd', 'Hg', 'Cn'], 30, 750, 'lightyellow'],
  ];
  for (const [symbols, first, dx, bg] of dBlock) {
    column(symbols, first, 129, d + dx, bg, (e) => (e === first ? 18 : 32));
  }

  const pBlock = [
    [['B', 'Al', 'Ga', 'In', 'Tl', 'Nh'], 5, 800, 'springgreen'],
    [['C', 'Si', 'Ge', 'Sn', 'Pb', 'Fl'], 6, 850, 'springgreen'],
    [['N', 'P', 'As', 'Sb', 'Bi', 'Mc'], 7, 900, 'springgreen'],
    [['O', 'S', 'Se', 'Te', 'Po', 'Lv'], 8, 950, 'springgreen'],
    [['F', 'Cl', 'Br', 'I', 'At', 'Ts'], 9, 1000, 'lightgreen'],
  ];
  for (const [symbols, first, dx, bg] of pBlock) {
    column(symbols, first, 43, d + dx, bg,
      (e) => (e === first ? 8 : e === first + 8 || e === first + 26 ? 18 : 32));
  }

  column(['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn', 'Og'], 2, 0, d + 1050, 'grey',
    (e) => (e === 2 || e === 10 ? 8 : e === 18 || e === 36 ? 18 : 32));

  ['Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu'].forEach((sym, i) =>
    elementButton(sym, 'pink', 58 + i, i * 50 + 400, 450));
  ['Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr'].forEach((sym, i) =>
    elementButton(sym, 'lightblue', 90 + i, i * 50 + 400, 493));

  new Button(rectangle_doc, { text: 'BACK', font: 'arial 11', bg: 'LIGHTBLUE', command: EXECUTION }).place({ x: 1300, y: 550 });
}

// FUNCTION TO PRESENT PERIODIC TABLE

function PERIODICTABLE() {
  CLEAR_SCREEN(180);
  const rectangle_doc = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  rectangle_doc.place({ x: 0, y: 180 });
  rectangle_doc.create_rectangle(0, 0, 2500, 2500);
  rectangle_doc.create_line(0, 2, 5000, 2);
  new Label(rectangle_doc, {
    text: 'ELEMENTS OF PERIODIC TABLE ARE', font: ' comicsansms 20 bold ', fg: '#FFFF00',
    bg: '#4169E1', borderwidth: 3, relief: RIDGE,
  }).place({ x: 10, y: 10 });
  new Label(rectangle_doc, {
    text: TABLE_TEXT,
    font: 'Courier 20 bold roman',
    fg: '#FAF9F6',
    bg: '#051047',
  }).place({ x: -250, y: 50 });

  new Button(rectangle_doc, { text: 'BACK', font: 'arial 11', bg: 'LIGHTBLUE', command: EXECUTION }).place({ x: 1300, y: 550 });
}

// FUNCTION EXECUTED AFTER LOGIN BUTTON IS PRESSED

function EXECUTION() {
  CLEAR_SCREEN();
  new Canvas(root, { bg: '#FFFFF0', height: 300, width: 1900 }).place({ x: 0, y: 0 });
  new Label(null, { text: 'PERIODIC TABLE', font: 'arial 40 bold', bg: '#FFFFF0' }).place({ x: 500, y: 70 });
  const rectangle_doc = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  rectangle_doc.place({ x: 0, y: 180 });
  rectangle_doc.create_rectangle(0, 0, 2500, 2500);
  rectangle_doc.create_line(0, 2, 5000, 2);

  // DISPLAYING BUTTONS FOR DIFFERENT FUNCTIONS

  const menuButton = (text, command, y) =>
    new Button(rectangle_doc, { text, width: 30, font: 'arial 30', fg: '#FFFF00', bg: '#4169E1', command }).place({ x: 350, y });
  menuButton('PERIODIC TABLE', PERIODICTABLE, 190);
  menuButton('ELEMENTAL GALLERY', PICTURES, 390);
  menuButton('ELEMENTAL INFORMATION', INFO_ELEMENTS, 90);
  menuButton('PERIODIC QUIZ', QUIZ_GAME, 290);
  menuButton('PLAY YOUR PART', USER_INFO, 490);
  new Button(root, { text: 'LOGOUT', font: 'arial 11', bg: 'LIGHTBLUE', command: BACK_TO_MAIN }).place({ x: 0, y: 185 });
}

// FUNCTION WILL VERIFY THAT USERNAME AND PASSWORD ENTER BY USER IS CORRECT OR NOT

function STUDENT_VERIFY() {
  let flag = 0;
  if (isnumeric(pre_CMS_var.get()) && len(strip(pre_CMS_var.get())) === 11) {
    for (const data of READ_LINES('students_account.txt')) {
      const data1 = stripNewlines(data).split('*');
      if (data1.length === 2 && strip(pre_CMS_var.get()) === data1[0] && strip(pre_pass_var.get()) === data1[1]) {
        flag = 1;
        break;
      }
    }
    if (flag === 1) EXECUTION();
    else tmsg.showinfo('Login', 'Account not found!');
  } else {
    tmsg.showinfo('Login', 'Invalid entries!');
  }
}

// FUNCTION FOR CREATING STUDENTS NEW ACCOUNT TO ACCESS PERIODIC TABLE

async function CREATE_ACCOUNT() {
  let signal = 1;

  // CHECKING WHETHER ACCOUNT ALREADY EXIST OR NOT

  if (isnumeric(new_CMS_var.get()) && len(new_CMS_var.get()) === 11) {
    for (const data of READ_LINES('students_account.txt')) {
      if (strip(data.split('*')[0]) === strip(new_CMS_var.get())) {
        tmsg.showinfo('Account', 'Account already exists!');
        signal = 0;
        break;
      }
    }
  }

  if (signal === 0) return;
  if (isnumeric(new_CMS_var.get()) && len(new_CMS_var.get()) === 11) {
    // THE LOGIN STRIPS SPACES AND '*' SEPARATES THE ID FROM THE PASSWORD IN THE FILE
    const password = strip(new_pass_var.get());
    if (!password || password.includes('*')) {
      tmsg.showinfo('Error', 'PASSWORD CAN NOT BE EMPTY OR CONTAIN * !');
      return;
    }
    open('students_account.txt', 'a').write(new_CMS_var.get() + '*' + password + '\n');
    await tmsg.showinfo('Account', 'ACCOUNT CREATED SUCCESSFULLY!');
    new_CMS_var.set('');
    new_pass_var.set('');
  } else {
    tmsg.showinfo('Error', 'CMS ID IS INVALID!');
  }
}

// WE HAVE TO CREATE THIS FUNCTION FOR LOGOUT PURPOSE

function main() {
  CLEAR_SCREEN();
  new Canvas(root, { bg: '#FFFFF0', height: 300, width: 1900 }).place({ x: 0, y: 0 });

  new Label(root, { text: ' MTH ', font: ['Segue UI', 44], fg: '#FFFF00', bg: '#051047' }).place({ x: 300, y: 45 });
  new Label(root, { text: 'PERIODIC TABLE ', font: ['Segue UI', 34], bg: '#FFFFF0' }).place({ x: 500, y: 50 });

  const rectangle_doc = new Canvas(root, { bg: '#051047', height: 700, width: 1900 });
  rectangle_doc.place({ x: 0, y: 180 });

  new Label(rectangle_doc, { text: 'CMS ID:', font: ['Segoe UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 350, y: 100 });
  new Label(rectangle_doc, { text: 'Password:', font: ['Segoe UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 350, y: 150 });

  // ALREADY PRESENT ACCOUNT

  pre_CMS_var = new StringVar();
  pre_pass_var = new StringVar();

  new Entry(rectangle_doc, { textvariable: pre_CMS_var, width: 30, font: 20 }).place({ x: 550, y: 110 });
  new Entry(rectangle_doc, { textvariable: pre_pass_var, width: 30, font: 20, show: '*' }).place({ x: 550, y: 160 });
  new Button(rectangle_doc, { text: 'Log in', font: 'arial 11', relief: GROOVE, command: STUDENT_VERIFY }).place({ x: 830, y: 200 });
  new Label(rectangle_doc, { text: 'STUDENT LOGIN', font: ['Segoe UI', 30], fg: '#FFFF00', bg: '#051047' }).place({ x: 550, y: 20 });

  // NEW ACCOUNT FOR STUDENT

  const line = new Canvas(rectangle_doc, { width: 1900, height: 5, bg: '#4169E1' });
  line.place({ x: 0, y: 250 });
  line.create_line(0, 10, 2500, 10, { fill: '#4169E1' });
  new Label(rectangle_doc, { text: 'PLEASE CREATE ACCOUNT TO ACCESS PERIODIC TABLE', font: ['Segue UI', 30], fg: '#FFFF00', bg: '#051047' }).place({ x: 250, y: 300 });
  new Label(rectangle_doc, { text: 'CMS ID:', font: ['Segue UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 350, y: 400 });
  new Label(rectangle_doc, { text: 'Password:', font: ['Segue UI', 24], fg: '#FFFF00', bg: '#051047' }).place({ x: 350, y: 450 });

  new_CMS_var = new StringVar();
  new_pass_var = new StringVar();

  new Entry(rectangle_doc, { textvariable: new_CMS_var, width: 30, font: 20 }).place({ x: 550, y: 405 });
  new Entry(rectangle_doc, { textvariable: new_pass_var, width: 30, font: 20, show: '*' }).place({ x: 550, y: 455 });
  new Button(rectangle_doc, { text: 'Create', font: 'arial 11', relief: GROOVE, command: CREATE_ACCOUNT }).place({ x: 830, y: 500 });
}

// FUNCTON FOR TKINTER

async function func() {
  // TKINTER MAIN WINDOW

  const stage = document.getElementById('root');
  root = new Tk(stage);
  root.geometry('1500x1000');
  root.title('PERIODIC TABLE');
  fitStage(stage);
  await loadFiles();
  main();
}

// OUR MAIN

func();
