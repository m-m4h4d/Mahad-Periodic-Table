"""Generate web/app/data.js from the literals in project/ESE.py.

The browser version shows exactly the same quiz questions and gallery names
as the desktop app, so this copies them out of ESE.py instead of duplicating
them by hand. Re-run after editing those lists:

    python scripts/extract_web_data.py
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
tree = ast.parse((ROOT / 'project' / 'ESE.py').read_text(encoding='utf8'))


def assigned_literal(func_name, var):
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == func_name)
    for node in ast.walk(func):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == var for t in node.targets):
            return ast.literal_eval(node.value)
    raise LookupError(f'{var} not found in {func_name}()')


def string_containing(func_name, needle):
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == func_name)
    return next(n.value for n in ast.walk(func)
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and needle in n.value)


data = {
    'IMAGE_FILES': assigned_literal('PICTURES', 'image_files'),
    'GALLERY_ELEMENTS': assigned_literal('PICTURES', 'elements'),
    'QUIZ_ELEMENTS': assigned_literal('QUIZ_GAME', 'elements'),
    'TABLE_TEXT': string_containing('PERIODICTABLE', 'COULMNS'),
}
out = ['// Generated from project/ESE.py by scripts/extract_web_data.py; do not edit.', '']
for name, value in data.items():
    out.append(f'export const {name} = {json.dumps(value, ensure_ascii=False, indent=2)};')
    out.append('')
(ROOT / 'web' / 'app' / 'data.js').write_text('\n'.join(out), encoding='utf8')
print({k: len(v) for k, v in data.items()})
