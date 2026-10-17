
# LIBRARIES WE HAD USED IN THIS PROJECT

from tkinter import *
from functools import partial
from tkinter import PhotoImage
from tkinter import StringVar
from tkinter.ttk import Entry
from tkinter import font as tkfont
import tkinter.messagebox as tmsg
import random
import os

# THE PROGRAM OPENS ITS PICTURES AND TEXT FILES BY NAME, SO WORK FROM ITS OWN FOLDER
# (THIS LETS IT START FROM ANY FOLDER, E.G. "python project/ESE.py")

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# STANDARD CMS ID LENGTH IS ELEVEN IN OUR PROJECT SUCH AS 00000000000

# ALL THE FUNCTIONS ARE GIVEN BELOW

# FUNCTION TO READ ALL LINES OF A TEXT FILE (NO LINES IF THE FILE DOES NOT EXIST YET)

def READ_LINES(file_name):
    try:
        with open(file_name, 'r', encoding='utf8') as f:
            return f.readlines()
    except FileNotFoundError:
        return []


# FUNCTION TO SPLIT TEXT INTO LINES THAT FIT IN THE GIVEN WIDTH (IN PIXELS)

def WRAP_TEXT(text, text_font, width):
    lines, line = [], ''
    for word in text.split():
        trial = f"{line} {word}" if line else word
        if line and text_font.measure(trial) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + [line]


# FUNCTION TO REMOVE THE WIDGETS OF THE PREVIOUS SCREEN SO THEY DO NOT PILE UP
# (WIDGETS PLACED HIGHER THAN from_y, LIKE THE TITLE, ARE KEPT)

def CLEAR_SCREEN(from_y=0):
    for widget in root.winfo_children():
        if int(widget.place_info().get('y', 0)) >= from_y:
            widget.destroy()

# FUNCTION TO LOGOUT

def BACK_TO_MAIN():
    ret = tmsg.askquestion("MAIN PAGE", "DO YOU WANT TO LOGOUT")
    if ret == 'yes':
        main()
    if ret == 'no':
        EXECUTION()


# FUNCTION FOR DISPLAYING INFORMATION ENTER BY USERS

def SEARCH_ALL():
    app_list.delete(0, END)
    student_count = 0
    detail_list = ['CMS ID:', 'NAME:', 'ELEMENT NAME:', 'INFORMATION:']
    for line in READ_LINES('user_element_info.txt'):
        if not line.strip():
            continue
        data = line.strip('\n').split('***')
        student_count += 1
        app_list.insert(END, ' ')
        app_list.insert(END, f" STUDENT : {student_count} :-")
        for index, i in enumerate(data[:len(detail_list)]):
            app_list.insert(END, f"{detail_list[index]} {i}")
    if student_count == 0:
        tmsg.showinfo("Sorry", "no information added yet!")


# FUNCTION FOR SEARCHING INFORMATION ENTER BY USER ON ELEMENT BASIS

def SEARCH_BY_ELEMENT():
    flag = 0
    if element_var.get().strip() == '':
        tmsg.showinfo("Error", "Invalid Entries!")
        return
    app_list.delete(0, END)
    student_count = 0
    detail_list = ['CMS ID:', 'NAME:', 'ELEMENT NAME:', 'INFORMATION:']
    for line in READ_LINES('user_element_info.txt'):
        data = line.strip('\n').split('***')
        if len(data) > 2 and data[2].strip().lower() == element_var.get().strip().lower():
            flag = 1
            student_count += 1
            app_list.insert(END, ' ')
            app_list.insert(END, f"DATA # : {student_count} :-")
            for index, i in enumerate(data[:len(detail_list)]):
                app_list.insert(END, f"{detail_list[index]} {i}")
    if flag == 0:
        tmsg.showinfo("Sorry", "element not found!")
    return


# FUNCTION FOR SEARCHING INFORMATION ENTER BY USER ON CMS ID BASIS

def DISPLAY_USER_INFO():
    flag = 0
    if len(str(cms1_var.get().strip())) != 11:
        tmsg.showinfo("Error", "Invalid Entries ... PLEASE TRY AGAIN !")
        return
    app_list.delete(0, END)
    student_count = 0
    detail_list = ['CMS ID:', 'NAME:', 'ELEMENT NAME:', 'INFORMATION:']
    for line in READ_LINES('user_element_info.txt'):
        data = line.strip('\n').split('***')
        if data[0].strip() == cms1_var.get().strip():
            flag = 1
            student_count += 1
            app_list.insert(END, ' ')
            app_list.insert(END, f"DATA # : {student_count} :-")
            for index, i in enumerate(data[:len(detail_list)]):
                app_list.insert(END, f"{detail_list[index]} {i}")
    if flag == 0:
        tmsg.showinfo("Sorry", "student not found!")
        return


# FUNCTION FOR DISPLAYING LAYOUT OF USER's INFORMATION

def SHOW_BUTTON():
    CLEAR_SCREEN(180)
    search_rectangle = Canvas(root, bg="#051047", height=700, width=1900)
    search_rectangle.place(x=0, y=180)
    Label(search_rectangle, text="SEARCH BY CMS ID:", font=('Segoe UI', 24), fg="#FFFF00", bg='#051047').place(x=20,
                                                                                                               y=20)
    Label(search_rectangle, text="SEARCH BY ELEMENT:", font=('Segoe UI', 24), fg="#FFFF00", bg='#051047').place(x=20,
                                                                                                                y=200)
    global cms1_var
    global element_var
    cms1_var = StringVar()
    element_var = StringVar()
    Entry(search_rectangle, textvariable=cms1_var, width=30, font=20).place(x=20, y=70)
    Entry(search_rectangle, textvariable=element_var, width=30, font=20).place(x=20, y=250)

    Button(search_rectangle, text="Search", font="SegoeUI 11", command=DISPLAY_USER_INFO).place(x=300, y=100)
    Button(search_rectangle, text="Search", font="SegoeUI 11", command=SEARCH_BY_ELEMENT).place(x=300, y=280)
    Button(search_rectangle, text="Search All", font="SegoeUI 25", height=1, width=10, command=SEARCH_ALL).place(x=100,
                                                                                                                 y=320)
    sby = Scrollbar(search_rectangle)
    global app_list
    app_list = Listbox(search_rectangle, height=10, width=70, font="SegoeUI 15", yscrollcommand=sby.set, fg="#FFFF00",
                       bg="#4169E1")
    app_list.place(x=500, y=150)
    sby.config(command=app_list.yview)
    sby.place(x=500 + app_list.winfo_reqwidth(), y=150, height=app_list.winfo_reqheight())

    Button(root, text="BACK", font="arial 11", bg="LIGHTBLUE", command=USER_INFO).place(x=1300, y=710)


# FUNCTION FOR WRITING USER INFORMATION IN TEXT FILE

def WRITING_USER_INFO():
    entries = [cms_var.get().strip(), user_name_var.get().strip(), ele_name_var.get().strip(),
               user_info_var.get().strip()]
    if not (entries[0].isnumeric() and len(entries[0]) == 11):
        tmsg.showinfo("Error", "CMS ID IS INVALID!")
        return
    if '' in entries:
        tmsg.showinfo("Error", "PLEASE FILL IN ALL THE FIELDS!")
        return
    if any('*' in entry for entry in entries):
        tmsg.showinfo("Error", "THE * CHARACTER IS NOT ALLOWED!")
        return

    with open("user_element_info.txt", 'a', encoding='utf8') as f:
        f.write('***'.join(entries) + '\n')
    tmsg.showinfo("information", "INFORMATION ADDED SUCCESSFULLY")
    user_info_var.set('')
    user_name_var.set('')
    ele_name_var.set('')
    cms_var.set('')


# FUNCTON THAT WILL ASK USER TO ENTER INFORMATION IF HE/SHE WANTS

def USER_INFO():
    CLEAR_SCREEN(180)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)
    Label(rectangle_doc, text="CMS ID", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=100)
    Label(rectangle_doc, text="NAME", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=200)
    Label(rectangle_doc, text="ELEMENT NAME", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=300)
    Label(rectangle_doc, text="INFORMATION", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=400)

    # DISPLAYING BUTTONS FOR INFORMATION ASKED BY USER

    global user_info_var
    global user_name_var
    global ele_name_var
    global cms_var
    user_info_var = StringVar()
    user_name_var = StringVar()
    ele_name_var = StringVar()
    cms_var = StringVar()
    Entry(rectangle_doc, textvariable=cms_var, width=30, font=20).place(x=750, y=100)
    Entry(rectangle_doc, textvariable=user_name_var, width=30, font=20).place(x=750, y=200)
    Entry(rectangle_doc, textvariable=ele_name_var, width=30, font=20).place(x=750, y=300)
    Entry(rectangle_doc, textvariable=user_info_var, width=30, font=20).place(x=750, y=400)
    Button(rectangle_doc, text="SAVE", font="arial 11", bg='lightblue', command=WRITING_USER_INFO).place(x=1040, y=450)
    Button(rectangle_doc, text="SHOW INFORMATION", font="arial 11", bg='lightblue', command=SHOW_BUTTON).place(x=750,
                                                                                                               y=450)

    Button(rectangle_doc, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=550)


# TO SEARCH IMAGE ON THE BASIS OF ITS ATOMIC NUMBER

def update_image():
    global image_index, name_label
    label.configure(image=images[image_index - 1])
    if name_label is not None:
        name_label.destroy()
    name_label = Label(root, text=elements[image_index - 1], width='15', font="SegoeUI 15 bold")
    name_label.place(x=500, y=679)


# FUNCTION TO GO TO NEXT IMAGE

def NEXT_IMAGE():
    global image_index
    image_index += 1
    if image_index > len(images):
        image_index = 1
    update_image()


# FUNCTION TO GO TO PREVIOUS IMAGE

def PREV_IMAGE():
    global image_index
    image_index -= 1
    if image_index < 1:
        image_index = len(images)
    update_image()


# FUNCTION UPDATE INDEX OF IMAGE

def UPDATE_INDEX():
    global image_index
    try:
        new_index = int(entry_var.get())
        if new_index < 1 or new_index > len(images):
            tmsg.showerror('Error', 'Invalid Atomic Number')
        else:
            image_index = new_index
            update_image()
    except ValueError:
        tmsg.showerror('Error', 'Invalid Atomic Number')


# FUNCTION TO PRESENT PICTURES OF ELEMENTS

def PICTURES():
    CLEAR_SCREEN(180)
    Label(text=" ELEMENTAL GALLERY ", font="SegueUI 40 bold", bg="#FFFFF0").place(x=350, y=70)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)

    # LIST OF ELEMENT PICTURES

    image_files = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png', '11.png',
                   '12.png', '13.png', '14.png', '15.png', '16.png', '17.png', '18.png', '19.png', '20.png', '21.png',
                   '22.png', '23.png', '24.png', '25.png', '26.png', '27.png', '28.png', '29.png', '30.png', '31.png',
                   '32.png', '33.png', '34.png', '35.png', '36.png', '37.png', '38.png', '39.png', '40.png', '41.png',
                   '42.png', '43.png', '44.png', '45.png', '46.png', '47.png', '48.png', '49.png', '50.png', '51.png',
                   '52.png', '53.png', '54.png', '55.png', '56.png', '57.png', '58.png', '59.png', '60.png', '61.png',
                   '62.png', '63.png', '64.png', '65.png', '66.png', '67.png', '68.png', '69.png', '70.png', '71.png',
                   '72.png', '73.png', '74.png', '75.png', '76.png', '77.png', '78.png', '79.png', '80.png', '81.png',
                   '82.png', '83.png', '84.png', '85.png', '86.png', '87.png', '88.png', '89.png', '90.png', '91.png',
                   '92.png', '93.png', '94.png', '95.png', '96.png', '97.png', '98.png', '99.png', '100.png', '101.png',
                   '102.png', '103.png', '104.png', '105.png', '106.png', '107.png', '108.png', '109.png', '110.png',
                   '111.png', '112.png', '113.png', '114.png', '115.png', '116.png', '117.png', '118.png']

    # LIST OF ELEMENT NAMES

    global elements

    elements = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine',
                'Neon', 'Sodium', 'Magnesium', 'Aluminum', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine', 'Argon',
                'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt',
                'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton',
                'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium', 'Ruthenium',
                'Rhodium', 'Palladium', 'Silver', 'Cadmium', 'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine',
                'Xenon', 'Cesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', 'Promethium',
                'Samarium', 'Europium', 'Gadolinium', 'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium',
                'Ytterbium', 'Lutetium', 'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum',
                'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', 'Radon', 'Francium', 'Radium',
                'Actinium', 'Thorium', 'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium',
                'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', 'Lawrencium',
                'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium',
                'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium', 'Moscovium', 'Livermorium', 'Tennessine',
                'Oganesson']

    global images
    images = [PhotoImage(file=f) for f in image_files]

    global image_index, name_label
    image_index = 1
    name_label = None

    # DISPLAYING BUTTONS FOR PICTURES TO MOVE FORWARD AND BACKWARD

    global label
    label = Label(root, image=images[0])
    label.place(x=500, y=250)
    Label(rectangle_doc, text=elements[image_index - 1], width='15', height='1', font="SegueUI 15 bold").place(x=500, y=500)
    Button(rectangle_doc, text='Previous', fg="#FFFF00", bg="#4169E1", width=10, height=1, command=PREV_IMAGE).place(
        x=10, y=400)
    Button(rectangle_doc, text='Next', fg="#FFFF00", bg="#4169E1", width=10, height=1, command=NEXT_IMAGE).place(x=100,
                                                                                                                 y=400)

    Label(rectangle_doc, text='ENTER THE ATOMIC NUMBER ', fg="#FFFF00", bg="#4169E1", font="SegueUI 15 bold").place(
        x=10, y=40)
    global entry_var
    entry_var = StringVar()
    Entry(rectangle_doc, textvariable=entry_var, width=30, font=('aerial', 10)).place(x=10, y=75)
    Button(rectangle_doc, text='Update', fg="#FFFF00", bg="#4169E1", width=10, height=1, command=UPDATE_INDEX).place(
        x=10, y=100)

    Button(rectangle_doc, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=550)


# TO CHECK ANS ENTER BY USER IS CORRECT OR NOT

def guess_check():
    root.title("QUIZ GAME")
    global score

    # REMOVE THE RESULT OF THE PREVIOUS ANSWER
    for widget in root.winfo_children():
        if getattr(widget, 'quiz_result', False):
            widget.destroy()

    if ANS_VAR.get().strip().lower() == element.lower():
        score += 10
        del elements[element]
        if not elements:
            tmsg.showinfo("quiz game", f"WELL DONE! YOU NAMED ALL THE ELEMENTS\nYOUR SCORE IS {score}")
            EXECUTION()
            return
        quiz()
        result = Label(text="CORRECT ANSWER", font=('Segue UI', 25), fg="#FFFF00", bg="#051047")
        result.quiz_result = True
        result.place(x=50, y=500 + quiz_shift)
    else:
        for text, y in (("WRONG ANSWER    ", 500), (f"YOUR SCORE IS {score}", 550)):
            result = Label(text=text, font=('Segue UI', 25), fg="#FFFF00", bg="#051047")
            result.quiz_result = True
            result.place(x=50, y=y + quiz_shift)
        ret = tmsg.askquestion("quiz game", "DO YOU WANT TO PLAY AGAIN")
        if ret == 'yes':
            QUIZ_GAME()
        if ret == 'no':
            EXECUTION()


# TO ASK QUIZ TO THE USER

def quiz():
    root.title("QUIZ GAME")
    global element
    element = random.choice(list(elements.keys()))

    # REMOVE THE PREVIOUS QUESTION
    for widget in root.winfo_children():
        if getattr(widget, 'quiz_question', False):
            widget.destroy()

    # DISPLAYING INFO FOR QUIZ IN LISTBOX
    # THE LIST IS WIDER THAN THE WINDOW, SO THE CLUE IS WRAPPED TO THE PART THAT CAN BE SEEN

    quiz_font = tkfont.Font(font="calibre 25")
    window_width = root.winfo_width() if root.winfo_width() > 1 else 1500
    indent = '    '
    wrap_width = min(80 * quiz_font.measure('0'), window_width - 50) - 30 - quiz_font.measure(indent)
    clue = WRAP_TEXT(f"Properties: {elements[element]['Properties']}", quiz_font, wrap_width)
    rows = ([f"Atomic Number: {elements[element]['Atomic Number']}"]
            + clue[:1] + [indent + line for line in clue[1:]]
            + [f"Symbol: {elements[element]['Symbol']}",
               f"Group: {elements[element]['Group']}",
               f"Period: {elements[element]['Period']}"])

    game_listbox = Listbox(root, width=80, height=len(rows), font=quiz_font, bg="lightblue")
    for row in rows:
        game_listbox.insert(END, row)
    game_listbox.place(x=50, y=200)

    # MOVE THE ANSWER BOX DOWN BY THE EXTRA LINES OF THE CLUE
    global quiz_shift
    quiz_shift = (len(rows) - 5) * quiz_font.metrics('linespace')

    question = [game_listbox, Label(text="ENTER THE ANSWER", font=('Se-geo UI', 25), fg="#FFFF00", bg="#051047")]
    question[1].place(x=50, y=445 + quiz_shift)
    global ANS_VAR
    ANS_VAR = StringVar()
    question.append(Entry(textvariable=ANS_VAR, width=30, font=20))
    question[2].place(x=450, y=450 + quiz_shift)
    question.append(Button(text="CHECK", font="arial 11", command=guess_check))
    question[3].place(x=720, y=500 + quiz_shift)

    question.append(Button(root, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION))
    question[4].place(x=1300, y=750)
    for widget in question:
        widget.quiz_question = True


# FUNCTION CONTAINING DATA FOR THE QUIZ

def QUIZ_GAME():
    root.title("QUIZ GAME")
    CLEAR_SCREEN(180)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)

    global score
    score = 0

    # CREATING NESTED DICTIONARY FOR QUIZ

    global elements

    elements = {
        "Hydrogen": {"Atomic Number": 1,
                     "Properties": "This element is the lightest and most abundant element in the universe. It is a "
                                   "colorless, flammable gas that combines with oxygen to form water.",
                     "Symbol": "H", "Group": 1, "Period": 1},
        "Helium": {"Atomic Number": 2,
                   "Properties": "This element is a colorless, odorless noble gas, the second most abundant element in"
                                 " the universe. It is used to fill balloons and to cool MRI magnets.",
                   "Symbol": "He", "Group": 18, "Period": 1},
        "Lithium": {"Atomic Number": 3,
                    "Properties": "This element is the lightest metal: a soft, silvery-white alkali metal that is "
                                  "highly reactive. It is used in rechargeable batteries.",
                    "Symbol": "Li", "Group": 1, "Period": 2},
        "Beryllium": {"Atomic Number": 4,
                      "Properties": "This element is a light, strong, steel-gray metal that is toxic to breathe in. It"
                                    " is used in aerospace parts, X-ray windows and copper alloys.",
                      "Symbol": "Be", "Group": 2, "Period": 2},
        "Boron": {"Atomic Number": 5,
                  "Properties": "This element is a hard, black metalloid. It is used in heat-resistant glass, cleaning"
                                " products and nuclear reactor control rods.",
                  "Symbol": "B", "Group": 13, "Period": 2},
        "Carbon": {"Atomic Number": 6,
                   "Properties": "This element is a nonmetal that forms more compounds than any other element. It "
                                 "occurs as soft graphite and as diamond, and is the basis of all known life.",
                   "Symbol": "C", "Group": 14, "Period": 2},
        "Nitrogen": {"Atomic Number": 7,
                     "Properties": "This element is a colorless, odorless, unreactive gas that makes up about 78% of "
                                   "the Earth's atmosphere. It is used to make ammonia for fertilizers.",
                     "Symbol": "N", "Group": 15, "Period": 2},
        "Oxygen": {"Atomic Number": 8,
                   "Properties": "This element is a colorless gas that makes up about 21% of the Earth's atmosphere. "
                                 "It is the third most abundant element in the universe and is needed for breathing "
                                 "and burning.",
                   "Symbol": "O", "Group": 16, "Period": 2},
        "Fluorine": {"Atomic Number": 9,
                     "Properties": "This element is a pale yellow gas and the most reactive and most electronegative "
                                   "element. Its compounds are added to toothpaste and used in non-stick coatings.",
                     "Symbol": "F", "Group": 17, "Period": 2},
        "Neon": {"Atomic Number": 10,
                 "Properties": "This element is a colorless, inert noble gas that glows reddish-orange in advertising "
                               "signs. It is the fifth most abundant element in the universe.",
                 "Symbol": "Ne", "Group": 18, "Period": 2},
        "Sodium": {"Atomic Number": 11,
                   "Properties": "This element is a soft, silvery-white alkali metal that can be cut with a knife and "
                                 "reacts vigorously with water. It is found in common table salt.",
                   "Symbol": "Na", "Group": 1, "Period": 3},
        "Magnesium": {"Atomic Number": 12,
                      "Properties": "This element is a light, silvery-white metal that burns with a brilliant white "
                                    "flame. It is used in lightweight alloys and is found at the center of "
                                    "chlorophyll.",
                      "Symbol": "Mg", "Group": 2, "Period": 3},
        "Aluminum": {"Atomic Number": 13,
                     "Properties": "This element is the most abundant metal in the Earth's crust: a light, "
                                   "silvery-white metal protected from corrosion by a thin oxide layer. It is used in "
                                   "cans, foil and aircraft.",
                     "Symbol": "Al", "Group": 13, "Period": 3},
        "Silicon": {"Atomic Number": 14,
                    "Properties": "This element is a hard, brittle metalloid with a blue-gray metallic luster. It is a"
                                  " semiconductor used in computer chips and solar cells, and the second most abundant"
                                  " element in the Earth's crust.",
                    "Symbol": "Si", "Group": 14, "Period": 3},
        "Phosphorus": {"Atomic Number": 15,
                       "Properties": "This element is a reactive nonmetal with several allotropes; its white form "
                                     "glows in the dark and catches fire in air. It is essential to life and used in "
                                     "matches and fertilizers.",
                       "Symbol": "P", "Group": 15, "Period": 3},
        "Sulfur": {"Atomic Number": 16,
                   "Properties": "This element is a yellow, brittle nonmetal that burns with a blue flame. It is used "
                                 "to vulcanize rubber and to make the most widely produced industrial acid.",
                   "Symbol": "S", "Group": 16, "Period": 3},
        "Chlorine": {"Atomic Number": 17,
                     "Properties": "This element is a pale yellow-green, toxic gas from the halogen group. It is used "
                                   "to disinfect drinking water and swimming pools, and makes up part of table salt.",
                     "Symbol": "Cl", "Group": 17, "Period": 3},
        "Argon": {"Atomic Number": 18,
                  "Properties": "This element is a colorless, odorless, inert noble gas that makes up about 0.93% of "
                                "the air, the third most abundant gas in the atmosphere. It is used in light bulbs and"
                                " welding.",
                  "Symbol": "Ar", "Group": 18, "Period": 3},
        "Potassium": {"Atomic Number": 19,
                      "Properties": "This element is a soft, silvery-white alkali metal that reacts violently with "
                                    "water and burns with a lilac flame. It is an essential nutrient found in bananas "
                                    "and fertilizers.",
                      "Symbol": "K", "Group": 1, "Period": 4},
        "Calcium": {"Atomic Number": 20,
                    "Properties": "This element is a soft, silvery-gray alkaline earth metal and the most abundant "
                                  "metal in the human body. It is found in bones, teeth, limestone and chalk.",
                    "Symbol": "Ca", "Group": 2, "Period": 4},
        "Scandium": {"Atomic Number": 21,
                     "Properties": "This element is a soft, silvery-white transition metal. Small amounts are added to"
                                   " aluminum to make strong, light alloys for aircraft and sports equipment.",
                     "Symbol": "Sc", "Group": 3, "Period": 4},
        "Titanium": {"Atomic Number": 22,
                     "Properties": "This element is a strong, light, silver-gray metal that resists corrosion. It is "
                                   "used in aircraft and medical implants, and its dioxide is a white pigment in "
                                   "paint.",
                     "Symbol": "Ti", "Group": 4, "Period": 4},
        "Vanadium": {"Atomic Number": 23,
                     "Properties": "This element is a hard, silvery-gray transition metal. It is added to steel to "
                                   "make tough, shock-resistant tools and springs, and its compounds come in many "
                                   "colors.",
                     "Symbol": "V", "Group": 5, "Period": 4},
        "Chromium": {"Atomic Number": 24,
                     "Properties": "This element is a hard, lustrous, steel-gray metal that takes a high polish. It is"
                                   " used for shiny plating and is the key ingredient that makes stainless steel "
                                   "rust-proof.",
                     "Symbol": "Cr", "Group": 6, "Period": 4},
        "Manganese": {"Atomic Number": 25,
                      "Properties": "This element is a hard, brittle, silvery-gray metal. It is essential for making "
                                    "steel and is used in alkaline batteries.",
                      "Symbol": "Mn", "Group": 7, "Period": 4},
        "Iron": {"Atomic Number": 26,
                 "Properties": "This element is a strong, gray metal that rusts in moist air. It is the main "
                               "ingredient of steel, makes up most of the Earth's core and carries oxygen in blood.",
                 "Symbol": "Fe", "Group": 8, "Period": 4},
        "Cobalt": {"Atomic Number": 27,
                   "Properties": "This element is a hard, lustrous, bluish-silver magnetic metal. It is used in "
                                 "superalloys, magnets and rechargeable batteries, and gives glass a deep blue color.",
                   "Symbol": "Co", "Group": 9, "Period": 4},
        "Nickel": {"Atomic Number": 28,
                   "Properties": "This element is a hard, silvery-white magnetic metal that resists corrosion. It is "
                                 "used in stainless steel, coins, plating and rechargeable batteries.",
                   "Symbol": "Ni", "Group": 10, "Period": 4},
        "Copper": {"Atomic Number": 29,
                   "Properties": "This element is a soft, reddish-orange metal and an excellent conductor of "
                                 "electricity. It is used in electrical wiring and pipes, turns green over time, and "
                                 "forms brass and bronze.",
                   "Symbol": "Cu", "Group": 11, "Period": 4},
        "Zinc": {"Atomic Number": 30,
                 "Properties": "This element is a bluish-white metal used to coat steel so that it does not rust "
                               "(galvanizing). With copper it forms brass, and it is an essential nutrient.",
                 "Symbol": "Zn", "Group": 12, "Period": 4},
        "Gallium": {"Atomic Number": 31,
                    "Properties": "This element is a soft, silvery metal that melts in your hand (at 29.8 degrees "
                                  "Celsius). It is used in semiconductors such as LEDs.",
                    "Symbol": "Ga", "Group": 13, "Period": 4},
        "Germanium": {"Atomic Number": 32,
                      "Properties": "This element is a hard, grayish-white metalloid and semiconductor. It was used in"
                                    " early transistors and is now used in fiber optics and infrared lenses.",
                      "Symbol": "Ge", "Group": 14, "Period": 4},
        "Arsenic": {"Atomic Number": 33,
                    "Properties": "This element is a gray metalloid famous as a poison. It is used in semiconductors "
                                  "for LEDs and was once used to preserve wood.",
                    "Symbol": "As", "Group": 15, "Period": 4},
        "Selenium": {"Atomic Number": 34,
                     "Properties": "This element is a nonmetal whose gray form conducts electricity better in light. "
                                   "It is used in photocopiers, glassmaking and solar cells, and is an essential trace"
                                   " nutrient.",
                     "Symbol": "Se", "Group": 16, "Period": 4},
        "Bromine": {"Atomic Number": 35,
                    "Properties": "This element is the only nonmetal that is liquid at room temperature: a dark "
                                  "red-brown halogen that gives off choking fumes. It is used in flame retardants.",
                    "Symbol": "Br", "Group": 17, "Period": 4},
        "Krypton": {"Atomic Number": 36,
                    "Properties": "This element is a colorless, odorless noble gas. It is used in some fluorescent "
                                  "lamps, photographic flash lamps and lasers.",
                    "Symbol": "Kr", "Group": 18, "Period": 4},
        "Rubidium": {"Atomic Number": 37,
                     "Properties": "This element is a very soft, silvery-white alkali metal that catches fire in air "
                                   "and reacts violently with water. It is used in atomic clocks.",
                     "Symbol": "Rb", "Group": 1, "Period": 5},
        "Strontium": {"Atomic Number": 38,
                      "Properties": "This element is a soft, silvery alkaline earth metal that turns yellowish in air."
                                    " Its compounds give fireworks and flares a bright red color.",
                      "Symbol": "Sr", "Group": 2, "Period": 5},
        "Yttrium": {"Atomic Number": 39,
                    "Properties": "This element is a soft, silvery transition metal. It is used in red phosphors for "
                                  "screens, in lasers and in superconductors.",
                    "Symbol": "Y", "Group": 3, "Period": 5},
        "Zirconium": {"Atomic Number": 40,
                      "Properties": "This element is a hard, silver-gray metal that resists corrosion. It is used to "
                                    "clad nuclear fuel rods, and its oxide is used to make imitation diamonds.",
                      "Symbol": "Zr", "Group": 4, "Period": 5},
        "Niobium": {"Atomic Number": 41,
                    "Properties": "This element is a soft, gray, ductile metal. It is used in superconducting magnets "
                                  "for MRI scanners and in strong steel for pipelines and jet engines.",
                    "Symbol": "Nb", "Group": 5, "Period": 5},
        "Molybdenum": {"Atomic Number": 42,
                       "Properties": "This element is a silvery metal with one of the highest melting points of all "
                                     "elements. It is used to make strong, heat-resistant steel and as a catalyst.",
                       "Symbol": "Mo", "Group": 6, "Period": 5},
        "Technetium": {"Atomic Number": 43,
                       "Properties": "This element was the first to be made artificially, and all of its isotopes are "
                                     "radioactive. It is a silvery-gray metal used in medical imaging.",
                       "Symbol": "Tc", "Group": 7, "Period": 5},
        "Ruthenium": {"Atomic Number": 44,
                      "Properties": "This element is a hard, brittle, silvery-white metal of the platinum group. It is"
                                    " used in electrical contacts, hard disk drives and as a catalyst.",
                      "Symbol": "Ru", "Group": 8, "Period": 5},
        "Rhodium": {"Atomic Number": 45,
                    "Properties": "This element is one of the rarest and most expensive metals: a silvery-white, "
                                  "highly reflective platinum-group metal. It is used in catalytic converters and "
                                  "jewelry plating.",
                    "Symbol": "Rh", "Group": 9, "Period": 5},
        "Palladium": {"Atomic Number": 46,
                      "Properties": "This element is a soft, silvery-white platinum-group metal that can soak up 900 "
                                    "times its own volume of hydrogen. It is used in catalytic converters and jewelry.",
                      "Symbol": "Pd", "Group": 10, "Period": 5},
        "Silver": {"Atomic Number": 47,
                   "Properties": "This element is a soft, lustrous white metal with the highest electrical and thermal"
                                 " conductivity of any element. It is used in jewelry, coins, mirrors and photography.",
                   "Symbol": "Ag", "Group": 11, "Period": 5},
        "Cadmium": {"Atomic Number": 48,
                    "Properties": "This element is a soft, bluish-white metal that is highly toxic. It is used in "
                                  "rechargeable batteries, yellow and red pigments, and nuclear reactor control rods.",
                    "Symbol": "Cd", "Group": 12, "Period": 5},
        "Indium": {"Atomic Number": 49,
                   "Properties": "This element is a very soft, silvery metal that makes a crying sound when bent. Its "
                                 "oxide mixed with tin oxide is the transparent conductor in touchscreens and LCDs.",
                   "Symbol": "In", "Group": 13, "Period": 5},
        "Tin": {"Atomic Number": 50,
                "Properties": "This element is a soft, silvery-white, malleable metal. It is used to coat steel food "
                              "cans, in solder, and with copper to make bronze.",
                "Symbol": "Sn", "Group": 14, "Period": 5},
        "Antimony": {"Atomic Number": 51,
                     "Properties": "This element is a brittle, silvery-blue metalloid. It is used in flame retardants "
                                   "and lead-acid batteries, and its sulfide was used as eye make-up in ancient times.",
                     "Symbol": "Sb", "Group": 15, "Period": 5},
        "Tellurium": {"Atomic Number": 52,
                      "Properties": "This element is a brittle, silvery-white metalloid and one of the rarest elements"
                                    " in the Earth's crust. It is used in thin-film solar panels and alloys.",
                      "Symbol": "Te", "Group": 16, "Period": 5},
        "Iodine": {"Atomic Number": 53,
                   "Properties": "This element is a shiny, violet-black nonmetal solid that turns straight into a "
                                 "violet vapor when heated. It is a halogen needed by the thyroid gland and used as an"
                                 " antiseptic.",
                   "Symbol": "I", "Group": 17, "Period": 5},
        "Xenon": {"Atomic Number": 54,
                  "Properties": "This element is a dense, colorless, odorless noble gas. It is used in bright car "
                                "headlamps, flash lamps and spacecraft ion engines, and as an anesthetic.",
                  "Symbol": "Xe", "Group": 18, "Period": 5},
        "Cesium": {"Atomic Number": 55,
                   "Properties": "This element is a soft, gold-colored alkali metal that melts at 28.5 degrees Celsius"
                                 " and explodes in water. It is used in atomic clocks that define the second.",
                   "Symbol": "Cs", "Group": 1, "Period": 6},
        "Barium": {"Atomic Number": 56,
                   "Properties": "This element is a soft, silvery alkaline earth metal. Its sulfate is swallowed to "
                                 "show the gut on X-rays, and its compounds give fireworks a green color.",
                   "Symbol": "Ba", "Group": 2, "Period": 6},
        "Lanthanum": {"Atomic Number": 57,
                      "Properties": "This element is a soft, silvery-white rare-earth metal that tarnishes quickly in "
                                    "air. It is used in hybrid car batteries and in high-quality camera lenses.",
                      "Symbol": "La", "Group": 3, "Period": 6},
        "Cerium": {"Atomic Number": 58,
                   "Properties": "This element is the most abundant rare-earth metal: a soft, iron-gray metal. It is "
                                 "used in lighter flints, for polishing glass and in catalytic converters.",
                   "Symbol": "Ce", "Group": "Lanthanides", "Period": 6},
        "Praseodymium": {"Atomic Number": 59,
                         "Properties": "This element is a soft, silvery rare-earth metal that gives glass a "
                                       "yellow-green color. It is used in welders' goggles, strong magnets and "
                                       "aircraft engine alloys.",
                         "Symbol": "Pr", "Group": "Lanthanides", "Period": 6},
        "Neodymium": {"Atomic Number": 60,
                      "Properties": "This element is a silvery rare-earth metal used to make the strongest permanent "
                                    "magnets, found in headphones, electric motors and wind turbines. It is also used "
                                    "in lasers.",
                      "Symbol": "Nd", "Group": "Lanthanides", "Period": 6},
        "Promethium": {"Atomic Number": 61,
                       "Properties": "This element is the only rare-earth metal with no stable isotopes, so all of it "
                                     "is radioactive. It has been used in nuclear batteries and luminous paint.",
                       "Symbol": "Pm", "Group": "Lanthanides", "Period": 6},
        "Samarium": {"Atomic Number": 62,
                     "Properties": "This element is a silvery rare-earth metal. With cobalt it makes strong magnets "
                                   "that keep working at high temperatures, and one of its isotopes is used to treat "
                                   "cancer.",
                     "Symbol": "Sm", "Group": "Lanthanides", "Period": 6},
        "Europium": {"Atomic Number": 63,
                     "Properties": "This element is the most reactive rare-earth metal: soft and silvery. Its "
                                   "compounds glow red and blue in screens, energy-saving lamps and anti-forgery marks"
                                   " on banknotes.",
                     "Symbol": "Eu", "Group": "Lanthanides", "Period": 6},
        "Gadolinium": {"Atomic Number": 64,
                       "Properties": "This element is a silvery rare-earth metal that is magnetic only below about 20 "
                                     "degrees Celsius. It is used as a contrast agent in MRI scans and for neutron "
                                     "shielding.",
                       "Symbol": "Gd", "Group": "Lanthanides", "Period": 6},
        "Terbium": {"Atomic Number": 65,
                    "Properties": "This element is a soft, silver-gray rare-earth metal. It is used in green phosphors"
                                  " for screens and lamps, and in alloys that change shape in a magnetic field.",
                    "Symbol": "Tb", "Group": "Lanthanides", "Period": 6},
        "Dysprosium": {"Atomic Number": 66,
                       "Properties": "This element is a soft, silvery rare-earth metal. It is added to the magnets in "
                                     "electric car motors and wind turbines so they keep working when hot.",
                       "Symbol": "Dy", "Group": "Lanthanides", "Period": 6},
        "Holmium": {"Atomic Number": 67,
                    "Properties": "This element is a soft, silvery rare-earth metal with the highest magnetic moment "
                                  "of any natural element. It is used in powerful magnets and medical lasers.",
                    "Symbol": "Ho", "Group": "Lanthanides", "Period": 6},
        "Erbium": {"Atomic Number": 68,
                   "Properties": "This element is a soft, silvery rare-earth metal whose compounds are pink. It is "
                                 "used to tint glass and to boost signals in fiber-optic cables.",
                   "Symbol": "Er", "Group": "Lanthanides", "Period": 6},
        "Thulium": {"Atomic Number": 69,
                    "Properties": "This element is one of the rarest rare-earth metals: soft and silvery enough to cut"
                                  " with a knife. It is used in portable X-ray machines and lasers.",
                    "Symbol": "Tm", "Group": "Lanthanides", "Period": 6},
        "Ytterbium": {"Atomic Number": 70,
                      "Properties": "This element is a soft, silvery rare-earth metal that slowly reacts with water "
                                    "and oxidizes in air. It is used in extremely precise atomic clocks and lasers.",
                      "Symbol": "Yb", "Group": "Lanthanides", "Period": 6},
        "Lutetium": {"Atomic Number": 71,
                     "Properties": "This element is the hardest and densest of the rare-earth metals: silvery-white, "
                                   "rare and expensive. It is used in PET scanners and cancer treatment.",
                     "Symbol": "Lu", "Group": "Lanthanides", "Period": 6},
        "Hafnium": {"Atomic Number": 72,
                    "Properties": "This element is a shiny, silvery, corrosion-resistant metal that absorbs neutrons "
                                  "well. It is used in nuclear reactor control rods, microchips and high-temperature "
                                  "alloys.",
                    "Symbol": "Hf", "Group": 4, "Period": 6},
        "Tantalum": {"Atomic Number": 73,
                     "Properties": "This element is a hard, dense, blue-gray metal that is almost completely immune to"
                                   " acids, even aqua regia. It is used in capacitors for phones and in surgical "
                                   "implants.",
                     "Symbol": "Ta", "Group": 5, "Period": 6},
        "Tungsten": {"Atomic Number": 74,
                     "Properties": "This element has the highest melting point of all metals (3422 degrees Celsius). "
                                   "It is very dense and is used in light-bulb filaments, X-ray tubes and cutting "
                                   "tools.",
                     "Symbol": "W", "Group": 6, "Period": 6},
        "Rhenium": {"Atomic Number": 75,
                    "Properties": "This element is one of the rarest metals: silvery-white, dense and with one of the "
                                  "highest melting points. It is used in jet engine superalloys and catalysts.",
                    "Symbol": "Re", "Group": 7, "Period": 6},
        "Osmium": {"Atomic Number": 76,
                   "Properties": "This element is the densest naturally occurring element: a hard, brittle, "
                                 "bluish-white metal. It is used in fountain-pen tips and electrical contacts, and its"
                                 " oxide is toxic.",
                   "Symbol": "Os", "Group": 8, "Period": 6},
        "Iridium": {"Atomic Number": 77,
                    "Properties": "This element is the most corrosion-resistant metal: hard, brittle, dense and "
                                  "silvery-white, unaffected by air, water and acids. It is used in spark plugs.",
                    "Symbol": "Ir", "Group": 9, "Period": 6},
        "Platinum": {"Atomic Number": 78,
                     "Properties": "This element is a dense, silvery-white precious metal and one of the least "
                                   "reactive metals. It is used in catalytic converters, jewelry, lab equipment and "
                                   "cancer drugs.",
                     "Symbol": "Pt", "Group": 10, "Period": 6},
        "Gold": {"Atomic Number": 79,
                 "Properties": "This element is a soft, yellow precious metal that never tarnishes. It is the most "
                               "malleable metal and is used in jewelry, coins and electronics.",
                 "Symbol": "Au", "Group": 11, "Period": 6},
        "Mercury": {"Atomic Number": 80,
                    "Properties": "This element is the only metal that is liquid at room temperature: shiny, silvery "
                                  "and toxic. It was used in thermometers and is used in fluorescent lamps.",
                    "Symbol": "Hg", "Group": 12, "Period": 6},
        "Thallium": {"Atomic Number": 81,
                     "Properties": "This element is a soft, gray metal that is highly toxic. It was once used in rat "
                                   "poison and insecticides, and is now used in electronics and heart scans.",
                     "Symbol": "Tl", "Group": 13, "Period": 6},
        "Lead": {"Atomic Number": 82,
                 "Properties": "This element is a soft, dense, bluish-gray metal that is toxic. It is used in car "
                               "batteries and to shield against radiation, and the Romans used it for water pipes.",
                 "Symbol": "Pb", "Group": 14, "Period": 6},
        "Bismuth": {"Atomic Number": 83,
                    "Properties": "This element is a brittle, pinkish-silver metal that forms rainbow-colored crystals"
                                  " and is the most diamagnetic metal. It expands when it freezes and is used in "
                                  "stomach medicine.",
                    "Symbol": "Bi", "Group": 15, "Period": 6},
        "Polonium": {"Atomic Number": 84,
                     "Properties": "This element is a rare, intensely radioactive, silvery-gray metal. It was "
                                   "discovered by Marie and Pierre Curie in 1898 and is used to remove static "
                                   "electricity.",
                     "Symbol": "Po", "Group": 16, "Period": 6},
        "Astatine": {"Atomic Number": 85,
                     "Properties": "This element is the rarest naturally occurring element in the Earth's crust: a "
                                   "highly radioactive halogen. Its chemistry is believed to be similar to iodine's.",
                     "Symbol": "At", "Group": 17, "Period": 6},
        "Radon": {"Atomic Number": 86,
                  "Properties": "This element is a colorless, radioactive noble gas and one of the densest gases. It "
                                "seeps from rocks into buildings and is a leading cause of lung cancer.",
                  "Symbol": "Rn", "Group": 18, "Period": 6},

        "Francium": {"Atomic Number": 87,
                     "Properties": "This element is an extremely rare, highly radioactive alkali metal; its most "
                                   "stable isotope lasts only about 22 minutes. It is used only in research.",
                     "Symbol": "Fr", "Group": 1,
                     "Period": 7},
        "Radium": {"Atomic Number": 88,
                   "Properties": "This element is an intensely radioactive, silvery-white alkaline earth metal that "
                                 "glows faint blue. It was discovered by the Curies and once used in glow-in-the-dark "
                                 "watch paint.",
                   "Symbol": "Ra", "Group": 2,
                   "Period": 7},
        "Actinium": {"Atomic Number": 89,
                     "Properties": "This element is a soft, silvery-white radioactive metal that glows pale blue in "
                                   "the dark. It is a powerful source of alpha rays and is being studied for cancer "
                                   "treatment.",
                     "Symbol": "Ac", "Group": 3,
                     "Period": 7},
        "Thorium": {"Atomic Number": 90,
                    "Properties": "This element is a weakly radioactive, silvery metal about three times as abundant "
                                  "as uranium. It could fuel nuclear reactors and was used in gas lantern mantles.",
                    "Symbol": "Th", "Group": "Actinides",
                    "Period": 7},
        "Protactinium": {"Atomic Number": 91,
                         "Properties": "This element is a rare, shiny, silver-gray radioactive metal that is very "
                                       "toxic. It is superconductive below 1.4 K and is used only in research.",
                         "Symbol": "Pa", "Group": "Actinides",
                         "Period": 7},
        "Uranium": {"Atomic Number": 92,
                    "Properties": "This element is a dense, weakly radioactive, silvery-gray metal and the heaviest "
                                  "element found in large amounts in nature. It fuels nuclear power plants and "
                                  "weapons.",
                    "Symbol": "U", "Group": "Actinides",
                    "Period": 7},

        "Neptunium": {"Atomic Number": 93,
                      "Properties": "This element was the first element heavier than uranium to be discovered (1940). "
                                    "It is a radioactive, silvery metal produced as a by-product in nuclear reactors.",
                      "Symbol": "Np", "Group": "Actinides", "Period": 7},
        "Plutonium": {"Atomic Number": 94,
                      "Properties": "This element is a radioactive, silvery metal made from uranium in nuclear "
                                    "reactors. It is used in nuclear weapons and to power spacecraft.",
                      "Symbol": "Pu", "Group": "Actinides", "Period": 7},
        "Americium": {"Atomic Number": 95,
                      "Properties": "This element is a synthetic, radioactive, silvery-white metal. A tiny amount of "
                                    "it is found in most household smoke detectors.",
                      "Symbol": "Am", "Group": "Actinides", "Period": 7},
        "Curium": {"Atomic Number": 96,
                   "Properties": "This element is a hard, dense, silvery radioactive metal named after a famous "
                                 "scientific couple. It has been used to power instruments on Mars rovers.",
                   "Symbol": "Cm", "Group": "Actinides", "Period": 7},
        "Berkelium": {"Atomic Number": 97,
                      "Properties": "This element is a synthetic, radioactive, silvery metal made only in tiny "
                                    "amounts. It is used as a target to create heavier elements such as element 117.",
                      "Symbol": "Bk", "Group": "Actinides", "Period": 7},
        "Californium": {"Atomic Number": 98,
                        "Properties": "This element is a synthetic, silvery-white radioactive metal soft enough to cut"
                                      " with a razor blade. It gives off neutrons and is used to start nuclear "
                                      "reactors.",
                        "Symbol": "Cf", "Group": "Actinides", "Period": 7},
        "Einsteinium": {"Atomic Number": 99,
                        "Properties": "This element was discovered in the debris of the first hydrogen bomb test in "
                                      "1952. It is made in milligram amounts by bombarding plutonium with neutrons in "
                                      "a reactor.",
                        "Symbol": "Es", "Group": "Actinides", "Period": 7},
        "Fermium": {"Atomic Number": 100,
                    "Properties": "This element is the heaviest element that can be made by bombarding lighter "
                                  "elements with neutrons, the last that can be made in visible amounts. It was found "
                                  "in hydrogen bomb debris.",
                    "Symbol": "Fm", "Group": "Actinides", "Period": 7},
        "Mendelevium": {"Atomic Number": 101,
                        "Properties": "This element is a synthetic radioactive metal of which only small amounts have "
                                      "ever been made. It is named after the creator of the periodic table.",
                        "Symbol": "Md", "Group": "Actinides", "Period": 7},
        "Nobelium": {"Atomic Number": 102,
                     "Properties": "This element is the second-to-last actinide: a synthetic, radioactive metal named "
                                   "after the inventor of dynamite. Little is known about its chemistry.",
                     "Symbol": "No", "Group": "Actinides", "Period": 7},
        "Lawrencium": {"Atomic Number": 103,
                       "Properties": "This element is the last actinide: a synthetic, radioactive metal used only for "
                                     "research. It is named after the inventor of the cyclotron.",
                       "Symbol": "Lr", "Group": "Actinides", "Period": 7},
        "Rutherfordium": {"Atomic Number": 104,
                          "Properties": "This element is the first element after the actinides. It is synthetic, "
                                        "radioactive and not found in nature, and is named after the father of nuclear"
                                        " physics.",
                          "Symbol": "Rf", "Group": 4, "Period": 7},
        "Dubnium": {"Atomic Number": 105,
                    "Properties": "This element is a synthetic, radioactive element with no uses outside research. It "
                                  "is named after a Russian town that is home to a nuclear research institute.",
                    "Symbol": "Db", "Group": 5, "Period": 7},
        "Seaborgium": {"Atomic Number": 106,
                       "Properties": "This element is a synthetic, radioactive element that behaves like a heavier "
                                     "version of tungsten. It was the first element named after a living person.",
                       "Symbol": "Sg", "Group": 6, "Period": 7},
        "Bohrium": {"Atomic Number": 107,
                    "Properties": "This element is a synthetic, radioactive element whose longest-lived atoms last "
                                  "only about a minute. It is named after the Danish physicist who modeled the atom.",
                    "Symbol": "Bh", "Group": 7, "Period": 7},
        "Hassium": {"Atomic Number": 108,
                    "Properties": "This element is a synthetic, radioactive element expected to behave like osmium. It"
                                  " is named after the German state where it was first made.",
                    "Symbol": "Hs", "Group": 8, "Period": 7},
        "Meitnerium": {"Atomic Number": 109,
                       "Properties": "This element is a synthetic, radioactive element first made in 1982; its atoms "
                                     "decay within seconds. It is named after a physicist who helped discover nuclear "
                                     "fission.",
                       "Symbol": "Mt", "Group": 9, "Period": 7},
        "Darmstadtium": {"Atomic Number": 110,
                         "Properties": "This element is a man-made element of which only a few atoms have been "
                                       "created, by fusing nickel and lead atoms in a heavy-ion accelerator. It has no"
                                       " uses outside research.",
                         "Symbol": "Ds", "Group": 10, "Period": 7},
        "Roentgenium": {"Atomic Number": 111,
                        "Properties": "This element is a man-made element made by fusing nickel and bismuth atoms in a"
                                      " heavy-ion accelerator. It is named after the discoverer of X-rays.",
                        "Symbol": "Rg", "Group": 11, "Period": 7},
        "Copernicium": {"Atomic Number": 112,
                        "Properties": "This element is a man-made element of which only a few atoms have been made, so"
                                      " it has no uses outside research. It is named after the astronomer who put the "
                                      "Sun at the center.",
                        "Symbol": "Cn", "Group": 12, "Period": 7},
        "Nihonium": {"Atomic Number": 113,
                     "Properties": "This element is the first element discovered in Asia (in Japan, 2004). It is "
                                   "synthetic, radioactive and expected to be a solid metal at room temperature.",
                     "Symbol": "Nh", "Group": 13, "Period": 7},
        "Flerovium": {"Atomic Number": 114,
                      "Properties": "This element is a synthetic, radioactive element first made in 1998 by firing "
                                    "calcium ions at plutonium in a particle accelerator.",
                      "Symbol": "Fl", "Group": 14, "Period": 7},
        "Moscovium": {"Atomic Number": 115,
                      "Properties": "This element is a synthetic, radioactive element about which little is known. It "
                                    "is expected to be a solid metal and decays quickly into element 113.",
                      "Symbol": "Mc", "Group": 15, "Period": 7},
        "Livermorium": {"Atomic Number": 116,
                        "Properties": "This element has no commercial uses; it has only been made in research, "
                                      "yielding insights into the behavior of superheavy atoms. It is named after a US"
                                      " laboratory.",
                        "Symbol": "Lv", "Group": 16, "Period": 7},
        "Tennessine": {"Atomic Number": 117,
                       "Properties": "This element is the heaviest known halogen: a synthetic, radioactive element "
                                     "first made in 2010. Only a few atoms have ever been produced.",
                       "Symbol": "Ts", "Group": 17, "Period": 7},
        "Oganesson": {"Atomic Number": 118,
                      "Properties": "This element is the heaviest known element: a synthetic, radioactive member of "
                                    "the noble gas group. Only a handful of atoms have been made, each lasting under a"
                                    " millisecond.",
                      "Symbol": "Og", "Group": 18, "Period": 7},

    }

    quiz()


# FUNCTION EXTRACTING INFORMATION FROM TEXT FILE OF ELEMENTS OF PERIODIC TABLE

def txtfile(k):
    root.title("info")
    CLEAR_SCREEN(180)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)

    ALL_COLUMNS = ['Atomic Number : ', 'Symbol : ', 'Element : ', 'Origin of name : ',
                   'Group : ', 'Period : ', 'Atomic weight : ', 'Density (g/cm^3): ',
                   'Melting point (K) : ', 'Boiling point (K): ',
                   'Specific heat capacity (J/g . K): ', 'Electronegativity : ',
                   'Abundance in earth\'s crust (mg/kg): ']

    # CREATING LISTBOX FOR DISPLAYING INFORMATION OF ELEMENTS

    info_listbox = Listbox(root, width=80, height=13, font="calibri 25", bg="lightblue")

    for line in READ_LINES("Periodictable.txt"):
        data = line.strip('\n').split('*')
        if str(k) == data[0].strip():
            for index, i in enumerate(data[:len(ALL_COLUMNS)]):
                info_listbox.insert(END, f"{ALL_COLUMNS[index]} {i}")
            break
    info_listbox.place(x=80, y=200)

    Button(text="BACK", font="arial 11", bg="LIGHTBLUE", command=INFO_ELEMENTS).place(x=1300, y=750)


# FUNCTON PASSING ARGUMENTS  TO ABOVE ONE FOR DISPLAYING INFORMATION OF ELEMENTS

def INFO_ELEMENTS():
    CLEAR_SCREEN(180)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)
    Label(rectangle_doc, text="f-BLOCK\nELEMENTS", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=200,
                                                                                                            y=445)
    Label(rectangle_doc, text="p-BLOCK\nELEMENTS", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=950, y=20)
    Label(rectangle_doc, text="d-BLOCK\nELEMENTS", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=600,
                                                                                                            y=100)
    Label(rectangle_doc, text="s-BLOCK\nELEMENTS", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=100,
                                                                                                            y=200)

    # USING A LOOP TO DISPLAY BUTTONS AND PASSING ATOMIC NUMBER AS ARGUMENTS

    elements = ['H', 'Li', 'Na', 'K', 'Rb', 'Cs', 'Fr']

    d = 100
    e = 1
    c = 0
    for i in range(7):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='orange',
               command=partial(txtfile, e)).place(x=d + 200, y=c + 100)
        if e == 1:
            e += 2
        elif e == 3 or e == 11:
            e += 8
        elif e == 19 or e == 37:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra']
    e = 4
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='yellow',
               command=partial(txtfile, e)).place(x=d + 250, y=c + 100)
        if e == 4 or e == 12:
            e += 8
        elif e == 20 or e == 38:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Sc', 'Y', 'La', 'Ac']
    e = 21
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 300, y=c + 100)
        if e == 21 or e == 39:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Ti', 'Zr', 'Hf', 'Rf']
    e = 22
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 350, y=c + 100)
        if (e == 22):
            e += 18
        else:
            e += 32
        c += 43

    elements = ['V', 'Nb', 'Ta', 'Db']
    e = 23
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 400, y=c + 100)
        if (e == 23):
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Cr', 'Mo', 'W', 'Sg']
    e = 24
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='lightyellow', command=partial(txtfile, e)).place(x=d + 450, y=c + 100)
        if e == 24:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Mn', 'Tc', 'Re', 'Bh']
    e = 25
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 500, y=c + 100)
        if e == 25:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Fe', 'Ru', 'Os', 'Hs']
    e = 26
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 550, y=c + 100)
        if e == 26:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Co', 'Rh', 'Ir', 'Mt']
    e = 27
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 600, y=c + 100)
        if e == 27:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Ni', 'Pd', 'Pt', 'Ds']
    e = 28
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='light yellow', command=partial(txtfile, e)).place(x=d + 650, y=c + 100)
        if e == 28:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Cu', 'Ag', 'Au', 'Rg']
    e = 29
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='lightyellow', command=partial(txtfile, e)).place(x=d + 700, y=c + 100)
        if e == 29:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['Zn', 'Cd', 'Hg', 'Cn']
    e = 30
    c = 129
    for i in range(4):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='lightyellow', command=partial(txtfile, e)).place(x=d + 750, y=c + 100)
        if e == 30:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['B', 'Al', 'Ga', 'In', 'Tl', 'Nh']
    e = 5
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='springgreen', command=partial(txtfile, e)).place(x=d + 800, y=c + 100)
        if e == 5:
            e += 8
        elif e == 13 or e == 31:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['C', 'Si', 'Ge', 'Sn', 'Pb', 'Fl']
    e = 6
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='springgreen', command=partial(txtfile, e)).place(x=d + 850, y=c + 100)
        if e == 6:
            e += 8
        elif e == 14 or e == 32:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['N', 'P', 'As', 'Sb', 'Bi', 'Mc']
    e = 7
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='springgreen', command=partial(txtfile, e)).place(x=d + 900, y=c + 100)
        if e == 7:
            e += 8
        elif e == 15 or e == 33:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['O', 'S', 'Se', 'Te', 'Po', 'Lv']
    e = 8
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='springgreen', command=partial(txtfile, e)).place(x=d + 950, y=c + 100)
        if e == 8:
            e += 8
        elif e == 16 or e == 34:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['F', 'Cl', 'Br', 'I', 'At', 'Ts']
    e = 9
    c = 43
    for i in range(6):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black',
               bg='lightgreen', command=partial(txtfile, e)).place(x=d + 1000, y=c + 100)
        if e == 9:
            e += 8
        elif e == 17 or e == 35:
            e += 18
        else:
            e += 32
        c += 43

    elements = ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn', 'Og']
    e = 2
    c = 0
    for i in range(7):
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='grey',
               command=partial(txtfile, e)).place(
            x=d + 1050, y=c + 100)
        if e == 2 or e == 10:
            e += 8
        elif e == 18 or e == 36:
            e += 18
        else:
            e += 32
        c += 43

    c = 0
    elements = ['Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    for i in range(14):
        e = 58 + i
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='pink',
               command=partial(txtfile, e)).place(x=c + 400, y=450)
        c += 50

    c = 0
    elements = ['Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr']
    for i in range(14):
        e = 90 + i
        Button(rectangle_doc, text=elements[i], width=5, height=2, font="Arial 10 bold", fg='black', bg='lightblue',
               command=partial(txtfile, e)).place(x=c + 400, y=493)
        c += 50

    Button(rectangle_doc, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=550)


# FUNCTION TO PRESENT PERIODIC TABLE

def PERIODICTABLE():
    CLEAR_SCREEN(180)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)
    rectangle_doc.create_rectangle(0, 0, 2500, 2500)
    rectangle_doc.create_line(0, 2, 5000, 2)
    Label(rectangle_doc, text='''ELEMENTS OF PERIODIC TABLE ARE''', font=" comicsansms 20 bold ", fg="#FFFF00"
          , bg="#4169E1", borderwidth=3, relief=RIDGE).place(x=10, y=10)
    Label(rectangle_doc, text='''     COULMNS
                                       
                                    1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18
                                    
                       R       1     H                                                  He
                       O       2     Li Be                               B  C  N  O  F  Ne
                       W       3     Na Mg                               Al Si P  S  Cl Ar
                       S       4     K  Ca Sc Ti V  Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr
                               5     Rb Sr Y  Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I  Xe
                               6     Cs Ba La Hf Ta W  Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn
                               7     Fr Ra Ac Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og

                     LANTHANIDES              Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu
                     ACTINIDES                Th Pa U  Np Pu Am Cm Bk Cf Es Fm Md No Lr''',
          font="Courier 20 bold roman",
          fg="#FAF9F6",
          bg="#051047").place(x=-250, y=50)

    Button(rectangle_doc, text="BACK", font="arial 11", bg="LIGHTBLUE", command=EXECUTION).place(x=1300, y=550)


# FUNCTION EXECUTED AFTER LOGIN BUTTON IS PRESSED

def EXECUTION():
    CLEAR_SCREEN()
    Canvas(root, bg="#FFFFF0", height=300, width=1900).place(x=0, y=0)
    Label(text="PERIODIC TABLE", font="arial 40 bold", bg="#FFFFF0").place(x=500, y=70)
    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)
    rectangle_doc.create_rectangle(0, 0, 2500, 2500)
    rectangle_doc.create_line(0, 2, 5000, 2)

    # DISPLAYING BUTTONS FOR DIFFERENT FUNCTIONS

    Button(rectangle_doc, text="PERIODIC TABLE", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=PERIODICTABLE).place(x=350, y=190)
    Button(rectangle_doc, text="ELEMENTAL GALLERY", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=PICTURES).place(x=350,
                                   y=390)
    Button(rectangle_doc, text="ELEMENTAL INFORMATION", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=INFO_ELEMENTS).place(x=350, y=90)
    Button(rectangle_doc, text="PERIODIC QUIZ", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=QUIZ_GAME).place(x=350, y=290)
    Button(rectangle_doc, text="PLAY YOUR PART", width=30, font="arial 30", fg="#FFFF00", bg="#4169E1",
           command=USER_INFO).place(x=350, y=490)
    Button(root, text="LOGOUT", font="arial 11", bg="LIGHTBLUE", command=BACK_TO_MAIN).place(x=0, y=185)


# FUNCTION WILL VERIFY THAT USERNAME AND PASSWORD ENTER BY USER IS CORRECT OR NOT

def STUDENT_VERIFY():
    flag = 0
    if str(pre_CMS_var.get()).isnumeric() and len(str(pre_CMS_var.get().strip())) == 11:
        for data in READ_LINES('students_account.txt'):
            data1 = data.strip('\n').split('*')
            if len(data1) == 2 and pre_CMS_var.get().strip() == data1[0] and pre_pass_var.get().strip() == data1[1]:
                flag = 1
                break
        if flag == 1:
            EXECUTION()
        else:
            tmsg.showinfo("Login", "Account not found!")
        return
    else:
        tmsg.showinfo("Login", "Invalid entries!")
        return


# FUNCTION FOR CREATING STUDENTS NEW ACCOUNT TO ACCESS PERIODIC TABLE

def CREATE_ACCOUNT():
    signal = 1

    # CHECKING WHETHER ACCOUNT ALREADY EXIST OR NOT

    if str(new_CMS_var.get()).isnumeric() and len(str(new_CMS_var.get())) == 11:
        for data in READ_LINES('students_account.txt'):
            if data.split('*')[0].strip() == new_CMS_var.get().strip():
                tmsg.showinfo("Account", "Account already exists!")
                signal = 0
                break

    if signal == 0:
        return
    if str(new_CMS_var.get()).isnumeric() and len(str(new_CMS_var.get())) == 11:
        # THE LOGIN STRIPS SPACES AND '*' SEPARATES THE ID FROM THE PASSWORD IN THE FILE
        password = new_pass_var.get().strip()
        if not password or '*' in password:
            tmsg.showinfo("Error", "PASSWORD CAN NOT BE EMPTY OR CONTAIN * !")
            return
        with open('students_account.txt', 'a', encoding='utf8') as b:
            b.write(new_CMS_var.get() + '*' + password + '\n')
        tmsg.showinfo("Account", "ACCOUNT CREATED SUCCESSFULLY!")
        new_CMS_var.set("")
        new_pass_var.set('')
        return
    else:
        tmsg.showinfo("Error", "CMS ID IS INVALID!")
        return


# WE HAVE TO CREATE THIS FUNCTION FOR LOGOUT PURPOSE

def main():
    global new_CMS_var, new_pass_var, pre_CMS_var, pre_pass_var
    CLEAR_SCREEN()

    Canvas(root, bg="#FFFFF0", height=300, width=1900).place(x=0, y=0)

    Label(root, text=" MTH ", font=('Segue UI', 44), fg="#FFFF00", bg="#051047").place(x=300, y=45)
    Label(root, text="PERIODIC TABLE ", font=('Segue UI', 34), bg='#FFFFF0').place(x=500, y=50)

    rectangle_doc = Canvas(root, bg="#051047", height=700, width=1900)
    rectangle_doc.place(x=0, y=180)

    Label(rectangle_doc, text="CMS ID:", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=100)
    Label(rectangle_doc, text="Password:", font=('Segoe UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=150)

    # ALREADY PRESENT ACCOUNT

    pre_CMS_var = StringVar()
    pre_pass_var = StringVar()

    Entry(rectangle_doc, textvariable=pre_CMS_var, width=30, font=20).place(x=550, y=110)
    Entry(rectangle_doc, textvariable=pre_pass_var, width=30, font=20, show='*').place(x=550, y=160)
    Button(rectangle_doc, text="Log in", font="arial 11", relief=GROOVE, command=STUDENT_VERIFY).place(x=830, y=200)
    Label(rectangle_doc, text="STUDENT LOGIN", font=('Segoe UI', 30), fg="#FFFF00", bg="#051047").place(x=550, y=20)

    # NEW ACCOUNT FOR STUDENT

    line = Canvas(rectangle_doc, width=1900, height=5, bg='#4169E1')
    line.place(x=0, y=250)
    line.create_line(0, 10, 2500, 10, fill='#4169E1')
    Label(rectangle_doc, text="PLEASE CREATE ACCOUNT TO ACCESS PERIODIC TABLE", font=('Segue UI', 30), fg="#FFFF00",
          bg="#051047").place(x=250,
                              y=300)
    Label(rectangle_doc, text="CMS ID:", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=400)
    Label(rectangle_doc, text="Password:", font=('Segue UI', 24), fg="#FFFF00", bg="#051047").place(x=350, y=450)

    new_CMS_var = StringVar()
    new_pass_var = StringVar()

    Entry(rectangle_doc, textvariable=new_CMS_var, width=30, font=20).place(x=550, y=405)
    Entry(rectangle_doc, textvariable=new_pass_var, width=30, font=20, show='*').place(x=550, y=455)
    Button(rectangle_doc, text="Create", font="arial 11", relief=GROOVE, command=CREATE_ACCOUNT).place(x=830, y=500)


# FUNCTON FOR TKINTER

def func():

    # TKINTER MAIN WINDOW

    global root
    root = Tk()
    root.geometry("1500x1000")
    root.title("PERIODIC TABLE")
    main()
    root.mainloop()


# OUR MAIN

func()
