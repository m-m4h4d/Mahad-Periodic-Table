"""Launcher for the MTH Periodic Table desktop app.

Checks that Python and Tkinter are available, then starts app/ESE.py from
inside its own folder (the app opens its pictures and text files by relative
path).
"""
import os
import runpy
import sys

APP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')

TK_HELP = {
    'win32': 'Re-run the Python installer from https://www.python.org/downloads/ and tick "tcl/tk and IDLE".',
    'darwin': 'Install Python from https://www.python.org/downloads/ (includes Tk), or run: brew install python-tk',
    'linux': 'Install Tk for Python, e.g. "sudo apt install python3-tk" or "sudo dnf install python3-tkinter".',
}


def fail(message):
    if sys.stderr:
        print(message, file=sys.stderr)
    elif sys.platform == 'win32':
        # Started with pythonw (no console): show a native message box instead.
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, message, 'MTH Periodic Table', 0x10)
    # Keep the console open when the launcher was double-clicked.
    if sys.stdin and sys.stdin.isatty():
        input('\nPress Enter to close...')
    sys.exit(1)


def main():
    if sys.version_info < (3, 6):
        fail('MTH Periodic Table needs Python 3.6 or newer (found %s).' % sys.version.split()[0])
    try:
        import tkinter  # noqa: F401
    except ImportError:
        platform = 'linux' if sys.platform.startswith('linux') else sys.platform
        fail('Tkinter is not available in this Python installation.\n'
             + TK_HELP.get(platform, TK_HELP['linux']))
    if not os.path.isfile(os.path.join(APP_DIR, 'ESE.py')):
        fail('Could not find app/ESE.py next to the launcher. Extract the whole zip and try again.')

    os.chdir(APP_DIR)
    sys.path.insert(0, APP_DIR)
    try:
        runpy.run_path('ESE.py', run_name='__main__')
    except Exception as exc:  # report crashes even when started without a console
        import traceback
        traceback.print_exc()
        try:
            import tkinter.messagebox
            tkinter.messagebox.showerror('MTH Periodic Table', 'The app stopped unexpectedly:\n\n%r' % exc)
        except Exception:
            pass
        fail('The app stopped unexpectedly.')


if __name__ == '__main__':
    main()
