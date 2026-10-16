# Mahad-Periodic-Table
Fundamentals of Information and Communication Technology end-semester project. This program is developed in Python. It tracks all elements in the periodic table along with the capability to add new elements to the list and search elements. Also includes a quiz to help chemistry students learn easily.

## Run it

### In your browser

The `web/` folder is a browser version of the same Tkinter app (same screens, layout, fonts and colours) with a landing page. It deploys to [Vercel](https://vercel.com) as a static site with no settings to change: import the repository and Vercel picks up `vercel.json`, which runs `scripts/build-web.sh` and serves `dist/`.

- `/` is the landing page, with buttons to open the app in the browser or download the desktop release.
- `/app/` is the app itself. Accounts and "Play your part" notes are saved in the browser (localStorage), starting from the sample data in `project/`.

To preview locally: `sh scripts/build-web.sh && python3 -m http.server -d dist`.

If you edit the quiz questions, gallery names or the text periodic table in `project/ESE.py`, run `python scripts/extract_web_data.py` to update `web/app/data.js`.

### On your desktop

Download `Mahad-Periodic-Table-desktop.zip` from the [latest release](https://github.com/m-m4h4d/Mahad-Periodic-Table/releases/latest), extract it and double-click the `Start Periodic Table` file for your system (or run `python3 launcher.py`). You need Python 3 with Tkinter.

You can also run it straight from the repository: `cd project && python ESE.py`.

### Publishing a release

Push a tag such as `v1.0.0` (or run the **Desktop release** workflow from the Actions tab). The workflow builds the zip with `scripts/build_release.py`, checks that the app starts, and attaches the zip to a GitHub release. Set the repository variable `WEB_URL` to your Vercel URL to include the browser link in the zip's README.
