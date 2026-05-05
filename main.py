import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

# ---------- Try importing tkinterdnd2 for drag-and-drop ----------
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

# ---------- CONSTANTS ----------
BG_MAIN      = "#f4f6f9"
BG_PANEL     = "#ffffff"
BG_CARD      = "#eef1f5"
BG_HOVER     = "#dce3ee"
ACCENT_BLUE  = "#1a73e8"
ACCENT_GREEN = "#188038"
ACCENT_RED   = "#c5221f"
TEXT_PRIMARY = "#1f2937"
TEXT_MUTED   = "#6b7280"
BORDER       = "#d1d5db"

FONT_TITLE   = ("Segoe UI", 22, "bold")
FONT_SUB     = ("Segoe UI", 10)
FONT_MONO    = ("Consolas", 9)
FONT_BTN     = ("Segoe UI Semibold", 9)
FONT_HEAD    = ("Segoe UI Semibold", 9)

# ---------- FILE STORE (path → iid) ----------
file_store: dict[str, str] = {}   # full_path → tree iid

# ---------- HASH FUNCTION ----------
def calculate_sha256(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"Error: {str(e)}"

# ---------- ACTIONS ----------
def add_entry(full_path):
    """Add a single file to the tree (skip duplicates)."""
    if full_path in file_store:
        return
    filename = os.path.basename(full_path)
    hash_val  = calculate_sha256(full_path)
    iid = tree.insert("", tk.END, values=(filename, full_path, hash_val, ""))
    file_store[full_path] = iid
    compare_hashes()
    update_status()

def add_files():
    files = filedialog.askopenfilenames(title="Select files to compare")
    for f in files:
        add_entry(f)

def on_drop(event):
    """Handle drag-and-drop event from tkinterdnd2."""
    raw = event.data
    # tkinterdnd2 wraps paths with spaces in braces; split accordingly
    paths = root.tk.splitlist(raw)
    for p in paths:
        p = p.strip()
        if os.path.isfile(p):
            add_entry(p)

def compare_hashes():
    children = tree.get_children()
    if not children:
        return
    hashes = [tree.item(i)["values"][2] for i in children]
    all_match = len(set(hashes)) == 1

    for item in children:
        if all_match:
            tree.set(item, "Status", "✔  MATCH")
            tree.item(item, tags=("match",))
        else:
            tree.set(item, "Status", "✘  MISMATCH")
            tree.item(item, tags=("mismatch",))

def clear_all():
    for item in tree.get_children():
        tree.delete(item)
    file_store.clear()
    update_status()

def remove_selected():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        vals = tree.item(item)["values"]
        full_path = vals[1] if len(vals) > 1 else None
        tree.delete(item)
        if full_path and full_path in file_store:
            del file_store[full_path]
    compare_hashes()
    update_status()

def copy_hash():
    selected = tree.selection()
    if not selected:
        return
    hash_val = tree.item(selected[0])["values"][2]
    root.clipboard_clear()
    root.clipboard_append(hash_val)
    set_status("Hash copied to clipboard ✔", color=ACCENT_GREEN)

def update_status():
    n = len(tree.get_children())
    set_status(f"{n} file{'s' if n != 1 else ''} loaded")

def set_status(msg, color=TEXT_MUTED):
    status_var.set(msg)
    status_label.configure(fg=color)

# ---------- BUTTON FACTORY ----------
def make_btn(parent, text, cmd, icon=""):
    label = f"{icon}  {text}" if icon else text
    btn = tk.Button(
        parent,
        text=label,
        command=cmd,
        bg=BG_CARD,
        fg=TEXT_PRIMARY,
        activebackground=ACCENT_BLUE,
        activeforeground="#ffffff",
        relief="flat",
        padx=14,
        pady=7,
        font=FONT_BTN,
        cursor="hand2",
        bd=0,
    )
    btn.bind("<Enter>", lambda e: btn.configure(bg=BG_HOVER))
    btn.bind("<Leave>", lambda e: btn.configure(bg=BG_CARD))
    return btn

# ---------- BUILD ROOT ----------
if DND_AVAILABLE:
    root = TkinterDnD.Tk()
else:
    root = tk.Tk()

root.title("SHA-256 File Comparator")
root.geometry("1100x620")
root.minsize(800, 480)
root.configure(bg=BG_MAIN)

# App icon (fallback: no icon)
try:
    root.iconbitmap(default="")
except Exception:
    pass

# ---------- STYLE ----------
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background=BG_CARD,
    foreground=TEXT_PRIMARY,
    rowheight=30,
    fieldbackground=BG_CARD,
    font=FONT_MONO,
    borderwidth=0,
)
style.configure("Treeview.Heading",
    background=BG_PANEL,
    foreground=ACCENT_BLUE,
    font=FONT_HEAD,
    relief="flat",
    padding=6,
)
style.map("Treeview",
    background=[("selected", "#1f4e79")],
    foreground=[("selected", "#ffffff")],
)
style.configure("Vertical.TScrollbar",
    background=BG_CARD,
    troughcolor=BG_PANEL,
    borderwidth=0,
    arrowcolor=TEXT_MUTED,
)

# ---------- HEADER ----------
header = tk.Frame(root, bg=BG_PANEL, pady=14)
header.pack(fill=tk.X, padx=0, pady=0)

title_lbl = tk.Label(
    header,
    text="🔐  SHA-256 File Comparator",
    bg=BG_PANEL,
    fg=TEXT_PRIMARY,
    font=FONT_TITLE,
)
title_lbl.pack(side=tk.LEFT, padx=24)

subtitle = tk.Label(
    header,
    text="Drag & drop files or use 'Add Files' to compare hashes",
    bg=BG_PANEL,
    fg=TEXT_MUTED,
    font=FONT_SUB,
)
subtitle.pack(side=tk.LEFT, padx=8, pady=4)

author_lbl = tk.Label(
    header,
    text="© Ashutosh Jha",
    bg=BG_PANEL,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9),
)
author_lbl.pack(side=tk.RIGHT, padx=24)

# ---------- SEPARATOR ----------
sep1 = tk.Frame(root, bg=BORDER, height=1)
sep1.pack(fill=tk.X)

# ---------- TOOLBAR ----------
toolbar = tk.Frame(root, bg=BG_MAIN, pady=10)
toolbar.pack(fill=tk.X, padx=16)

make_btn(toolbar, "Add Files",        add_files,       "📂").pack(side=tk.LEFT, padx=4)
make_btn(toolbar, "Copy Hash",        copy_hash,       "📋").pack(side=tk.LEFT, padx=4)
make_btn(toolbar, "Remove Selected",  remove_selected, "🗑").pack(side=tk.LEFT, padx=4)
make_btn(toolbar, "Clear All",        clear_all,       "✖").pack(side=tk.LEFT, padx=4)

if not DND_AVAILABLE:
    tk.Label(
        toolbar,
        text="⚠  Install tkinterdnd2 for drag-and-drop support",
        bg=BG_MAIN,
        fg="#e3b341",
        font=("Segoe UI", 9),
    ).pack(side=tk.RIGHT, padx=8)

# ---------- DROP ZONE BANNER (visible only if DnD available) ----------
if DND_AVAILABLE:
    drop_banner = tk.Label(
        root,
        text="⬇   Drop files anywhere in this window",
        bg="#e8f0fe",
        fg=ACCENT_BLUE,
        font=("Segoe UI", 9, "italic"),
        pady=5,
    )
    drop_banner.pack(fill=tk.X, padx=16)

# ---------- TABLE FRAME ----------
table_frame = tk.Frame(root, bg=BG_MAIN)
table_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=(6, 0))

columns = ("File", "Path", "SHA-256", "Status")

tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="extended")

tree.heading("File",   text="File Name")
tree.heading("Path",   text="Full Path")
tree.heading("SHA-256",text="SHA-256 Hash")
tree.heading("Status", text="Status")

tree.column("File",    width=180, minwidth=120)
tree.column("Path",    width=320, minwidth=160)
tree.column("SHA-256", width=430, minwidth=200)
tree.column("Status",  width=120, minwidth=80, anchor="center")

scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL,   command=tree.yview)
scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=tree.xview)
tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

scrollbar_y.pack(side=tk.RIGHT,  fill=tk.Y)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
tree.pack(fill=tk.BOTH, expand=True)

# Row tags
tree.tag_configure("match",    background="#e6f4ea", foreground="#188038")
tree.tag_configure("mismatch", background="#fce8e6", foreground="#c5221f")

# ---------- DRAG-AND-DROP REGISTRATION ----------
if DND_AVAILABLE:
    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", on_drop)

# ---------- STATUS BAR ----------
sep2 = tk.Frame(root, bg=BORDER, height=1)
sep2.pack(fill=tk.X, pady=(6, 0))

status_bar = tk.Frame(root, bg=BG_PANEL, pady=5)
status_bar.pack(fill=tk.X, side=tk.BOTTOM)

status_var = tk.StringVar(value="No files loaded")
status_label = tk.Label(
    status_bar,
    textvariable=status_var,
    bg=BG_PANEL,
    fg=TEXT_MUTED,
    font=("Segoe UI", 9),
    anchor="w",
)
status_label.pack(side=tk.LEFT, padx=12)

# ---------- KEYBOARD SHORTCUTS ----------
root.bind("<Delete>",         lambda e: remove_selected())
root.bind("<Control-o>",      lambda e: add_files())
root.bind("<Control-w>",      lambda e: remove_selected())
root.bind("<Control-c>",      lambda e: copy_hash())

# ---------- MAIN LOOP ----------
root.mainloop()