// A tiny Tkinter look-alike for the browser.
//
// It reproduces just enough of tkinter (as rendered on Windows) to run a
// line-by-line port of project/ESE.py: widgets are absolutely positioned with
// .place(), nothing is ever destroyed, and newer widgets stack on top of older
// ones, exactly like the desktop app.

export const END = 'end';
export const RIDGE = 'ridge';
export const GROOVE = 'groove';

// Windows "SystemButtonFace"
const SYS = '#F0F0F0';

// ---------------------------------------------------------------- colours

// Tk resolves colour names with the X11 table on every platform; only the
// names whose X11 value differs from CSS need translating.
const X11 = { grey: '#BEBEBE', gray: '#BEBEBE', green: '#00FF00', maroon: '#B03060', purple: '#A020F0' };

function color(name) {
  if (!name) return name;
  const key = String(name).toLowerCase().replace(/\s+/g, '');
  return X11[key] || key;
}

function rgb(c) {
  const probe = document.createElement('i');
  probe.style.color = c;
  document.body.appendChild(probe);
  const m = getComputedStyle(probe).color.match(/\d+/g).map(Number);
  probe.remove();
  return m;
}

const hex = (r, g, b) => '#' + [r, g, b].map((v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0')).join('');

// 3-D border shades, following Tk's TkpGetShadows / the Windows system colours.
const shadeCache = new Map();
function shades(bg) {
  const c = color(bg || SYS);
  if (shadeCache.has(c)) return shadeCache.get(c);
  let s;
  if (c.toLowerCase() === SYS.toLowerCase()) {
    s = { light: '#FFFFFF', lightInner: '#E3E3E3', dark: '#A0A0A0', darkest: '#696969' };
  } else {
    const [r, g, b] = rgb(c);
    const lt = (v) => Math.max(Math.min(255, v * 1.4), (255 + v) / 2);
    s = {
      light: hex(lt(r), lt(g), lt(b)),
      lightInner: hex((lt(r) + r) / 2, (lt(g) + g) / 2, (lt(b) + b) / 2),
      dark: hex(r * 0.6, g * 0.6, b * 0.6),
      darkest: hex(r * 0.4, g * 0.4, b * 0.4),
    };
  }
  shadeCache.set(c, s);
  return s;
}

// A 2px Windows-style relief drawn with inset shadows.
function relief(bg, kind) {
  const s = shades(bg);
  const band = (tl1, br1, tl2, br2) =>
    `inset 1px 1px 0 ${tl1}, inset -1px -1px 0 ${br1}, inset 2px 2px 0 ${tl2}, inset -2px -2px 0 ${br2}`;
  switch (kind) {
    case 'sunken': return band(s.dark, s.light, s.darkest, s.lightInner);
    case 'groove': return band(s.dark, s.light, s.light, s.dark);
    case 'ridge': return band(s.light, s.dark, s.dark, s.light);
    case 'flat': return 'none';
    default: return band(s.light, s.darkest, s.lightInner, s.dark);
  }
}

// ---------------------------------------------------------------- fonts

const STACK = {
  segoe: '"Segoe UI", "Segoe UI Variable Text", system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif',
  arial: 'Arial, "Liberation Sans", Arimo, "Helvetica Neue", Helvetica, sans-serif',
  calibri: 'Calibri, Carlito, Arial, "Liberation Sans", sans-serif',
  courier: '"Courier New", "Liberation Mono", Cousine, Courier, monospace',
};
// Tk's linespace (ascent + descent) for each family, in em.
const LINESPACE = { segoe: 1.33, arial: 1.15, calibri: 1.22, courier: 1.133 };

// Families Windows actually has; anything else (typos such as "Segue UI",
// "SegoeUI", "calibre", "aerial") falls back to Arial, as GDI does.
function family(name) {
  const f = String(name).toLowerCase().trim();
  if (f === 'segoe ui') return 'segoe';
  if (f === 'arial') return 'arial';
  if (f === 'calibri') return 'calibri';
  if (f === 'courier' || f === 'courier new') return 'courier';
  return 'arial';
}

// Accepts the same specs ESE.py uses: ('Segoe UI', 24), "arial 30 bold", 20 ...
export function font(spec) {
  if (spec == null) return { fam: 'segoe', size: 9, bold: false, italic: false }; // TkDefaultFont
  let parts;
  if (Array.isArray(spec)) parts = spec.map(String);
  else parts = String(spec).trim().split(/\s+/);
  const fam = family(parts[0]);
  const size = parts[1] !== undefined && !isNaN(parseFloat(parts[1])) ? Math.abs(parseFloat(parts[1])) : 12;
  const rest = parts.slice(2).map((p) => p.toLowerCase());
  return { fam, size, bold: rest.includes('bold'), italic: rest.includes('italic') };
}

function applyFont(el, spec) {
  const f = font(spec);
  el.style.fontFamily = STACK[f.fam];
  el.style.fontSize = f.size + 'pt';
  el.style.fontWeight = f.bold ? '700' : '400';
  el.style.fontStyle = f.italic ? 'italic' : 'normal';
  el.style.lineHeight = String(LINESPACE[f.fam]);
  return LINESPACE[f.fam];
}

// ---------------------------------------------------------------- variables

export class StringVar {
  constructor(value = '') {
    this.value = String(value);
    this.watchers = new Set();
  }
  get() { return this.value; }
  set(v) {
    this.value = String(v);
    this.watchers.forEach((w) => w(this.value));
  }
}

// ---------------------------------------------------------------- root

let ROOT = null;

export class Tk {
  constructor(stage) {
    ROOT = this;
    this.el = stage;
    this.inner = stage;
    stage.classList.add('tk-root');
  }
  title(t) { document.title = t; }
  geometry(g) {
    const m = /^(\d+)x(\d+)/.exec(g);
    if (m) {
      this.el.style.width = m[1] + 'px';
      this.el.style.height = m[2] + 'px';
      window.dispatchEvent(new Event('resize'));
    }
  }
}

// ---------------------------------------------------------------- widgets

class Widget {
  constructor(master, opts, tag) {
    this.master = master || ROOT;
    this.el = document.createElement(tag);
    this.opts = {};
    this.configure(opts || {});
  }
  configure(opts) {
    Object.assign(this.opts, opts);
    this.render();
  }
  render() {}
  place({ x = 0, y = 0 } = {}) {
    this.el.style.left = x + 'px';
    this.el.style.top = y + 'px';
    if (!this.el.isConnected) this.master.inner.appendChild(this.el);
    return this;
  }
}

export class Canvas extends Widget {
  constructor(master, opts) {
    super(master, opts, 'div');
    this.el.className = 'tk-canvas';
    this.items = document.createElement('div');
    this.items.className = 'tk-canvas-items';
    this.el.appendChild(this.items);
    this.inner = this.el;
  }
  render() {
    const o = this.opts;
    this.el.style.width = (o.width ?? 378) + 'px';
    this.el.style.height = (o.height ?? 265) + 'px';
    this.el.style.background = color(o.bg || SYS);
  }
  // Canvas coordinates start under the 2px highlight ring.
  _item(x1, y1, w, h, css) {
    const d = document.createElement('div');
    Object.assign(d.style, { left: x1 - 2 + 'px', top: y1 - 2 + 'px', width: w + 'px', height: h + 'px' }, css);
    this.items.appendChild(d);
  }
  create_line(x1, y1, x2, y2, opts = {}) {
    const fill = color(opts.fill || 'black');
    if (y1 === y2) this._item(Math.min(x1, x2), y1, Math.abs(x2 - x1), 1, { background: fill });
    else if (x1 === x2) this._item(x1, Math.min(y1, y2), 1, Math.abs(y2 - y1), { background: fill });
  }
  create_rectangle(x1, y1, x2, y2, opts = {}) {
    this._item(x1, y1, x2 - x1, y2 - y1, {
      boxSizing: 'border-box',
      border: `1px solid ${color(opts.outline || 'black')}`,
      background: opts.fill ? color(opts.fill) : 'transparent',
    });
  }
}

export class Label extends Widget {
  constructor(master, opts) {
    super(master, opts, 'div');
  }
  render() {
    const o = this.opts;
    const el = this.el;
    el.className = 'tk-label';
    const bg = color(o.bg || SYS);
    const bd = o.borderwidth ?? o.bd ?? 2;
    el.style.background = bg;
    el.style.color = color(o.fg || 'black');
    if (o.relief && o.relief !== 'flat') {
      el.style.border = `${bd}px ${o.relief} ${bg}`;
    } else {
      el.style.border = `${bd}px solid ${bg}`;
    }
    el.style.padding = '1px';
    if (o.image) {
      let img = el.querySelector('img');
      if (!img) {
        el.textContent = '';
        img = document.createElement('img');
        img.alt = '';
        img.draggable = false;
        el.appendChild(img);
      }
      if (img.getAttribute('src') !== o.image) img.src = o.image;
      el.style.width = el.style.height = '';
      return;
    }
    const lh = applyFont(el, o.font);
    el.textContent = '';
    const span = document.createElement('span');
    span.textContent = o.text ?? '';
    el.appendChild(span);
    el.style.width = o.width ? `${Number(o.width)}ch` : '';
    el.style.height = o.height ? `${Number(o.height) * lh}em` : '';
  }
}

export class Button extends Widget {
  constructor(master, opts) {
    super(master, opts, 'button');
    this.el.type = 'button';
    this.el.addEventListener('click', () => {
      if (this.opts.command) this.opts.command();
    });
  }
  render() {
    const o = this.opts;
    const el = this.el;
    el.className = 'tk-button';
    const bg = color(o.bg || SYS);
    el.style.background = bg;
    el.style.color = color(o.fg || 'black');
    el.style.setProperty('--raised', relief(bg, o.relief || 'raised'));
    el.style.setProperty('--sunken', relief(bg, 'sunken'));
    const lh = applyFont(el, o.font);
    el.textContent = '';
    const span = document.createElement('span');
    span.textContent = o.text ?? '';
    el.appendChild(span);
    el.style.width = o.width ? `${Number(o.width)}ch` : '';
    el.style.height = o.height ? `${Number(o.height) * lh}em` : '';
  }
}

export class Entry extends Widget {
  constructor(master, opts) {
    super(master, opts, 'input');
    const el = this.el;
    el.type = 'text';
    el.className = 'tk-entry';
    el.spellcheck = false;
    el.autocomplete = 'off';
    this.real = '';
    const v = this.opts.textvariable;
    if (v) {
      this._show(v.get());
      v.watchers.add((val) => {
        if (val !== this.real) this._show(val);
      });
    }
    // With show='*' keep the real text aside and display asterisks, as Tk does.
    el.addEventListener('beforeinput', (e) => {
      if (!this.opts.show) return;
      e.preventDefault();
      let s = el.selectionStart, t = el.selectionEnd;
      let txt = this.real;
      const data = e.data ?? (e.dataTransfer ? e.dataTransfer.getData('text/plain') : '');
      switch (e.inputType) {
        case 'insertText': case 'insertReplacementText': case 'insertFromPaste': case 'insertFromDrop':
          txt = txt.slice(0, s) + (data || '').replace(/[\r\n]/g, '') + txt.slice(t); s += (data || '').length; break;
        case 'deleteContentBackward':
          if (s === t && s > 0) s -= 1;
          txt = txt.slice(0, s) + txt.slice(t); break;
        case 'deleteContentForward':
          if (s === t) t += 1;
          txt = txt.slice(0, s) + txt.slice(t); break;
        case 'deleteWordBackward': case 'deleteSoftLineBackward': case 'deleteHardLineBackward':
          txt = txt.slice(t); s = 0; break;
        case 'deleteWordForward': case 'deleteSoftLineForward': case 'deleteHardLineForward':
          txt = txt.slice(0, s); break;
        case 'deleteByCut':
          txt = txt.slice(0, s) + txt.slice(t); break;
        default: return;
      }
      this._commit(txt);
      el.setSelectionRange(s, s);
    });
    el.addEventListener('input', () => {
      if (!this.opts.show) this._commit(el.value);
    });
    // Tk entries don't copy out of a masked field.
    el.addEventListener('copy', (e) => { if (this.opts.show) e.preventDefault(); });
    el.addEventListener('cut', (e) => { if (this.opts.show) e.preventDefault(); });
  }
  _commit(txt) {
    this.real = txt;
    if (this.opts.show) this.el.value = this.opts.show[0].repeat(txt.length);
    if (this.opts.textvariable) this.opts.textvariable.set(txt);
  }
  _show(val) {
    this.real = val;
    this.el.value = this.opts.show ? this.opts.show[0].repeat(val.length) : val;
  }
  render() {
    const o = this.opts;
    applyFont(this.el, o.font ?? ['Segoe UI', 9]);
    this.el.style.width = `${o.width ?? 20}ch`;
  }
}

export class Listbox extends Widget {
  constructor(master, opts) {
    super(master, opts, 'div');
    const el = this.el;
    el.className = 'tk-listbox';
    el.tabIndex = 0;
    this.rows = [];
    this.top = 0;
    this.selected = -1;
    el.addEventListener('wheel', (e) => {
      e.preventDefault();
      if (e.deltaY) this.yview_scroll(e.deltaY > 0 ? 4 : -4);
    }, { passive: false });
    el.addEventListener('mousedown', (e) => {
      const row = e.target.closest('.tk-row');
      const i = row ? this.rows.indexOf(row) : this.rows.length - 1;
      if (i < 0) return;
      if (this.selected >= 0 && this.rows[this.selected]) this.rows[this.selected].classList.remove('sel', 'active');
      this.selected = i;
      this.rows[i].classList.add('sel', 'active');
    });
  }
  render() {
    const o = this.opts;
    const el = this.el;
    this.lh = applyFont(el, o.font);
    el.style.background = color(o.bg || 'white');
    el.style.color = color(o.fg || 'black');
    el.style.width = `${o.width ?? 20}ch`;
    el.style.height = `${(o.height ?? 10) * this.lh}em`;
  }
  insert(where, text) {
    const row = document.createElement('div');
    row.className = 'tk-row';
    // Tk draws control characters such as the trailing "\n" as nothing.
    row.textContent = String(text).replace(/[\r\n]/g, '');
    this.el.appendChild(row);
    this.rows.push(row);
    this._sync();
  }
  delete(first, last) {
    if (first === 0 && last === END) {
      this.rows.forEach((r) => r.remove());
      this.rows = [];
      this.top = 0;
      this.selected = -1;
      this._sync();
    }
  }
  size() { return this.rows.length; }
  get(i) { return this.rows[i]?.textContent ?? ''; }
  _visible() { return Math.max(1, this.opts.height ?? 10); }
  _sync() {
    const max = Math.max(0, this.rows.length - this._visible());
    this.top = Math.max(0, Math.min(this.top, max));
    const rowPx = this.rows[0] ? this.rows[0].offsetHeight : 0;
    this.el.scrollTop = this.top * rowPx;
    const n = this.rows.length;
    const first = n ? this.top / n : 0;
    const last = n ? Math.min(1, (this.top + this._visible()) / n) : 1;
    if (this.opts.yscrollcommand) this.opts.yscrollcommand(first, last);
  }
  yview_scroll(n) {
    this.top += n;
    this._sync();
  }
  yview(...args) {
    if (args[0] === 'scroll') this.yview_scroll(Number(args[1]));
    else if (args[0] === 'moveto') {
      this.top = Math.round(Number(args[1]) * this.rows.length);
      this._sync();
    }
  }
}

export class Scrollbar extends Widget {
  constructor(master, opts) {
    super(master, opts, 'div');
    const el = this.el;
    el.className = 'tk-scrollbar disabled';
    const up = document.createElement('div');
    const down = document.createElement('div');
    up.className = 'arrow up';
    down.className = 'arrow down';
    el.append(up, down);
    const press = (n) => () => this.opts.command && this.opts.command('scroll', n, 'units');
    up.addEventListener('mousedown', press(-1));
    down.addEventListener('mousedown', press(1));
    this.set = (first, last) => el.classList.toggle('disabled', first <= 0 && last >= 1);
  }
  config(opts) { this.configure(opts); }
}

// ---------------------------------------------------------------- messagebox

const ICONS = {
  info: '<svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="15" fill="#1C6FD1"/><circle cx="16" cy="9" r="2.2" fill="#fff"/><rect x="14.2" y="13" width="3.6" height="12" rx="1" fill="#fff"/></svg>',
  error: '<svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="15" fill="#E81123"/><path d="M10.5 10.5l11 11M21.5 10.5l-11 11" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg>',
  question: '<svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="15" fill="#1C6FD1"/><path d="M12 12.5a4 4 0 1 1 5.6 3.7c-1 .5-1.6 1.2-1.6 2.3v1" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/><circle cx="16" cy="23.5" r="1.7" fill="#fff"/></svg>',
};

function dialog(kind, title, message, buttons, closeValue) {
  return new Promise((resolve) => {
    const shade = document.createElement('div');
    shade.className = 'tk-modal';
    const box = document.createElement('div');
    box.className = 'tk-dialog';
    box.setAttribute('role', 'alertdialog');
    box.setAttribute('aria-modal', 'true');
    box.innerHTML = `
      <div class="tk-dialog-title"><span></span><button type="button" class="tk-dialog-close" aria-label="Close">✕</button></div>
      <div class="tk-dialog-body"><div class="tk-dialog-icon">${ICONS[kind]}</div><div class="tk-dialog-text"></div></div>
      <div class="tk-dialog-buttons"></div>`;
    box.querySelector('.tk-dialog-title span').textContent = title;
    box.querySelector('.tk-dialog-text').textContent = message;
    const row = box.querySelector('.tk-dialog-buttons');
    const prevFocus = document.activeElement;
    const done = (value) => {
      document.removeEventListener('keydown', onKey, true);
      shade.remove();
      if (prevFocus && prevFocus.focus) prevFocus.focus();
      resolve(value);
    };
    const btns = buttons.map(([label, value]) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'tk-dialog-button';
      b.textContent = label;
      b.addEventListener('click', () => done(value));
      row.appendChild(b);
      return b;
    });
    const close = box.querySelector('.tk-dialog-close');
    if (closeValue === undefined) close.disabled = true;
    else close.addEventListener('click', () => done(closeValue));
    const onKey = (e) => {
      if (e.key === 'Escape' && closeValue !== undefined) { e.preventDefault(); done(closeValue); }
      else if (e.key === 'Tab') {
        e.preventDefault();
        const i = btns.indexOf(document.activeElement);
        btns[(i + (e.shiftKey ? btns.length - 1 : 1)) % btns.length].focus();
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        const i = btns.indexOf(document.activeElement);
        btns[(i + (e.key === 'ArrowLeft' ? btns.length - 1 : 1)) % btns.length].focus();
      } else if (!box.contains(e.target)) { e.preventDefault(); }
    };
    document.addEventListener('keydown', onKey, true);
    shade.appendChild(box);
    document.body.appendChild(shade);
    btns[0].focus();
  });
}

export const messagebox = {
  showinfo: (title, message) => dialog('info', title, message, [['OK', 'ok']], 'ok'),
  showerror: (title, message) => dialog('error', title, message, [['OK', 'ok']], 'ok'),
  askquestion: (title, message) => dialog('question', title, message, [['Yes', 'yes'], ['No', 'no']]),
};

// ---------------------------------------------------------------- misc

// functools.partial
export const partial = (fn, ...bound) => (...rest) => fn(...bound, ...rest);

// The window is 1500x1000 like the desktop app; shrink it to fit small screens.
export function fitStage(stage) {
  const fit = () => {
    const w = stage.offsetWidth;
    const h = stage.offsetHeight;
    const s = Math.min(1, window.innerWidth / w);
    stage.style.transform = s < 1 ? `scale(${s})` : '';
    stage.parentElement.style.height = h * s + 'px';
    stage.parentElement.style.width = w * s + 'px';
  };
  window.addEventListener('resize', fit);
  fit();
}
