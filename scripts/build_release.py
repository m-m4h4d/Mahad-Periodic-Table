"""Package the Tkinter desktop app as a zip for a GitHub release.

    python scripts/build_release.py [VERSION] [--web-url URL]

Writes release/Mahad-Periodic-Table-desktop.zip containing the launcher,
start scripts for Windows/macOS/Linux and the app itself under app/.
"""
import argparse
import stat
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = 'Mahad-Periodic-Table'
APP_FILES = ['ESE.py', 'Periodictable.txt', 'students_account.txt', 'user_element_info.txt']
EXECUTABLE = {'start-linux.sh', 'Start Periodic Table (macOS).command'}


def add(zf, arcname, data, executable=False):
    info = zipfile.ZipInfo(f'{NAME}/{arcname}', date_time=(2024, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    mode = 0o755 if executable else 0o644
    info.external_attr = (stat.S_IFREG | mode) << 16
    zf.writestr(info, data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('version', nargs='?', default='dev')
    parser.add_argument('--web-url', default='')
    args = parser.parse_args()

    out = ROOT / 'release' / f'{NAME}-desktop.zip'
    out.parent.mkdir(exist_ok=True)
    project = ROOT / 'project'
    images = sorted(project.glob('*.png'), key=lambda p: (not p.stem.isdigit(), int(p.stem) if p.stem.isdigit() else 0, p.name))

    with zipfile.ZipFile(out, 'w') as zf:
        for path in sorted((ROOT / 'desktop').iterdir()):
            if not path.is_file() or path.name == 'RELEASE_NOTES.md':
                continue
            data = path.read_bytes()
            if path.name == 'README.txt':
                text = data.decode('utf8').replace('{version}', args.version.lstrip('v'))
                if args.web_url:
                    text = text.replace('{web_url}', args.web_url)
                else:
                    text = text.replace('Prefer not to install anything? Use the browser version:\n  {web_url}\n\n', '')
                data = text.replace('\n', '\r\n').encode('utf8')
            add(zf, path.name, data, path.name in EXECUTABLE)
        for name in APP_FILES:
            add(zf, f'app/{name}', (project / name).read_bytes())
        for path in images:
            add(zf, f'app/{path.name}', path.read_bytes())
        add(zf, 'LICENSE.txt', (ROOT / 'LICENSE').read_bytes())

    print(f'{out.relative_to(ROOT)}: {out.stat().st_size / 1e6:.1f} MB, {len(images)} images')


if __name__ == '__main__':
    main()
