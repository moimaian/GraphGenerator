# GraphGenerator

**GraphGenerator** is a desktop tool (Python + PySide6/Qt) that turns a
**CSV or XLSX table into a chart**: bar, line, scatter, stacked/overlapped
area, box plot, violin, histogram, density (KDE) and heatmap in **1D**
(one or more Y series against a categorical or numeric X), plus numeric
**2D** and **3D** scatter/line/area. Trendlines (linear/quadratic/cubic,
moving average, logarithmic, exponential) with R² and equation, legends,
color palettes and value labels are all optional per chart. It runs on
**Linux and Windows**, has **light / dark themes** and a
**Portuguese / English** switch.

Version: [`versao.py`](versao.py) is the single source of truth (shown in
the app header as "Version X.Y.Z-N"). Bump rules — MAJOR / MINOR / PATCH
plus the `-N` packaging revision — are in
[`installer/VERSIONING.md`](installer/VERSIONING.md); every bump also needs
a matching top entry in
[`installer/linux/changelog.Debian`](installer/linux/changelog.Debian)
(`build_deb.sh` refuses to package if the two disagree).

---

## Install

### Linux — `GraphGenerator.deb`

A ready-to-use package sits at the repository root, next to this README:

```bash
sudo apt install ./GraphGenerator.deb
#  or:  sudo dpkg -i ./GraphGenerator.deb && sudo apt -f install
```

Installs the app under `/usr/share/graphgenerator/`, a
`/usr/bin/graphgenerator` launcher, the menu entry with icons, and a Desktop
shortcut. **It needs internet access once, during installation:** the
`postinst` builds a private virtual environment in
`/usr/lib/graphgenerator/venv` and downloads `PySide6`, `numpy`, `pandas`,
`matplotlib`, `seaborn` and `openpyxl` into it from PyPI. The system Python
is never touched, so it works on distros that block global `pip install`
(PEP 668: Ubuntu 23.04+/24.04, Debian 12+). Requires `python3 >= 3.10` and
`python3-venv` (pulled in automatically, along with the Qt system libraries
such as `libxcb-cursor0`).

If you installed offline (or that download failed), the app tells you when
you try to open it; fix it later, with internet, by running:

```bash
sudo graphgenerator-setup
```

To rebuild the package yourself: `installer/build_deb.sh` (writes
`./GraphGenerator.deb`).

### Run from source

Requires **Python 3.10+**:

```bash
pip install --user -r requirements.txt
python3 GraphGenerator.py
```

Double-clicking [`GraphGenerator.py`](GraphGenerator.py) (or running it with
any Python 3) also works standalone, without `requirements.txt`: the script
**bootstraps its own virtual environment** on first run — it creates a
`GraphGenerator/` venv next to itself (needs Python **3.10** available as
`python3.10`), installs every dependency into it, and re-executes itself
inside that venv. This only happens when the script's own folder is
writable (e.g. running straight from a git checkout). The `.deb` doesn't
rely on it: its launcher already runs the app from the venv built at
install time, and the script detects it is inside a venv and does nothing.

### Windows

Run from source the same way (`pip install -r requirements.txt` then
`python3 GraphGenerator.py`), or just double-click `GraphGenerator.py` with
Python installed — the self-bootstrap described above creates its own venv
and installs everything automatically on first launch.

---

## Interface

One window: a header (icon · `GraphGenerator` · version · light/dark toggle
· 🇧🇷 / 🇬🇧) and, below it, the chart form.

1. **Title**, **input file** (CSV/XLSX, via *Select data file…*) and
   **Dimensions** (`1D` / `2D` / `3D`, mutually exclusive).
2. **Select Columns** — three lists (X / Y / Z) whose content adapts to the
   chosen dimension:
   - **1D**: X accepts *any* column (categorical, for classes/frequency
     counts when no Y is picked; or numeric, e.g. an "epoch"/index column
     to plot against one or more Y series). Y accepts one or more numeric
     columns (multi-select) — pick several to compare them on the same
     chart. Z is disabled.
   - **2D**: X is one numeric column; Y accepts one **or more** numeric
     columns (multi-select), plotted against that shared numeric X axis.
   - **3D**: X, Y and Z are each exactly one numeric column.
3. **Chart type** — options depend on the dimension: 1D offers Bar, Line,
   Scatter, Area (Stacked/Overlapped), Box Plot, Heatmap, Violin, Histogram
   and Density (KDE); 2D offers Scatter, Line and Area
   (Stacked/Overlapped); 3D is Scatter only.
4. **Resolution (dpi)**, **trendline** (with optional legend equation +
   R²), **show legend**, **show value labels**, **colors** (single color or
   a named palette) and optional **axis labels**.
5. **Generate chart** opens the result in a separate window (matplotlib's
   Qt canvas + toolbar), from which it can be exported as
   PNG/JPG/TIFF/PDF/EPS/SVG at the chosen DPI.

If the loaded table has a `Class`/`Classes`/`Group`/`Groups` column, 2D
Scatter with a single Y series colors and labels points by that column
automatically.

---

## Data loading

[`load_xy_table`](GraphGenerator.py) reads CSV (auto-detects `pt-BR`
`;`-separated, comma-decimal files and converts them to clean `en-US` CSV)
and XLSX/XLS (via `openpyxl`). Column classification for 1D
(`_is_column_numeric`) treats a column as numeric when at least half its
values parse as a number (comma or dot decimal) — everything else is
treated as categorical/text.

---

## Project layout

```
GraphGenerator.py    single-file app: bootstrap, data loading, matplotlib
                      plot functions (1D/2D/3D), Qt UI (GraphGeneratorUI)
versao.py             single source of truth for the version
i18n.py                PT/EN strings for the header and form — t(key, lang)
preferencias.py       ~/.config/graphgenerator/config.json (language, theme)
estilo.py              light/dark palettes + class-based QSS
Midia/
  GraphGenerator_Icon.png   app icon (header, window, Menu/Desktop shortcut)
installer/                        scripts that BUILD the installer (not the installer itself)
  build_deb.sh, linux/            Linux .deb packaging (linux/graphgenerator-setup builds the venv)
  VERSIONING.md                   MAJOR/MINOR/PATCH rules + changelog sync
GraphGenerator.deb                ready-to-use Linux installer (built by installer/build_deb.sh)
requirements.txt                  pip dependencies for running from source
```

Language and theme are saved to `~/.config/graphgenerator/config.json` and
restored on the next launch. Set `GRAPHGENERATOR_CONFIG_DIR` to use an
isolated config (handy for testing); set `QT_QPA_PLATFORM=offscreen` to run
headless.

---

## License

GraphGenerator is free software licensed under the **GNU General Public
License v3.0 or later** (GPL-3.0-or-later). See [`LICENSE`](LICENSE) for the
full text.

Copyright © 2026 Moisés Maia Neto &lt;moimaian@gmail.com&gt;

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.
