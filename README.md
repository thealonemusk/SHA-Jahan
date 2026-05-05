# 🔐 SHA-Jahan — SHA-256 File Comparator

A modern desktop tool to compare SHA-256 hashes of multiple files side by side.  
Built with Python + Tkinter. Supports drag-and-drop, full file paths, and one-click hash copying.

---

## ✨ Features

- 📂 Add files via dialog or **drag & drop**
- 🗂 Displays **file name**, **full path**, and **SHA-256 hash**
- ✔ / ✘ Auto status — **MATCH** or **MISMATCH** across all loaded files
- 📋 Copy any hash to clipboard
- ⌨️ Keyboard shortcuts (`Ctrl+O`, `Delete`, `Ctrl+C`)
- 🎨 Modern dark UI (GitHub-inspired)

---

## 🚀 Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/thealonemusk/sha-jahan.git
cd sha-jahan
```

### 2. Install dependencies

```bash
pip install tkinterdnd2
```

### 3. Run the app

```bash
python main.py
```

---

## 📦 Build Executable (.exe)

### Prerequisites

```bash
pip install pyinstaller tkinterdnd2
```

### Option 1 — Single `.exe` file (recommended)

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="SHA-Jahan" main.py
```

> The `.exe` will be in the `dist/` folder.

---

### Option 2 — Single `.exe` with drag-and-drop support

`tkinterdnd2` ships native DLL files that PyInstaller needs to bundle manually.  
Use this command to ensure DnD works in the final exe:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="SHA-Jahan" ^
  --collect-data tkinterdnd2 ^
  main.py
```

On **Linux/macOS**, replace `^` with `\`:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name="SHA-Jahan" \
  --collect-data tkinterdnd2 \
  main.py
```

---

### Option 3 — Folder build (faster startup, easier debugging)

```bash
pyinstaller --windowed --icon=icon.ico --name="SHA-Jahan" --collect-data tkinterdnd2 main.py
```

> Output will be in `dist/SHA-Jahan/`. Share the entire folder.

---

### Option 4 — Using a `.spec` file (full control)

Generate the spec first:

```bash
pyi-makespec --onefile --windowed --icon=icon.ico --name="SHA-Jahan" main.py
```

Then edit `SHA-Jahan.spec` to add:

```python
from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('tkinterdnd2')
```

Then build:

```bash
pyinstaller SHA-Jahan.spec
```

---

### Clean build artifacts

```bash
# Windows
rmdir /s /q build dist __pycache__
del SHA-Jahan.spec

# macOS / Linux
rm -rf build dist __pycache__ SHA-Jahan.spec
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + O` | Add files |
| `Ctrl + C` | Copy selected hash |
| `Delete` | Remove selected row |

---

## 🛠 Tech Stack

- Python 3.x
- Tkinter (built-in GUI)
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2) — drag-and-drop support
- PyInstaller — for building the `.exe`

---

## 👤 Author

**Ashutosh Jha** — [@thealonemusk](https://github.com/thealonemusk)
