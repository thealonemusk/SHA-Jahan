import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os

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
def add_files():
    files = filedialog.askopenfilenames()
    for file in files:
        filename = os.path.basename(file)
        hash_val = calculate_sha256(file)
        tree.insert("", tk.END, values=(filename, hash_val, ""))
    compare_hashes()

def compare_hashes():
    hashes = [tree.item(i)['values'][1] for i in tree.get_children()]
    if not hashes:
        return

    all_match = all(h == hashes[0] for h in hashes)

    for item in tree.get_children():
        if all_match:
            tree.set(item, "Status", "MATCH")
            tree.item(item, tags=("match",))
        else:
            tree.set(item, "Status", "MISMATCH")
            tree.item(item, tags=("mismatch",))

def clear_all():
    for item in tree.get_children():
        tree.delete(item)

def remove_selected():
    selected = tree.selection()
    if not selected:
        return
    for item in selected:
        tree.delete(item)
    compare_hashes()

def copy_hash():
    selected = tree.selection()
    if not selected:
        return
    hash_val = tree.item(selected[0])['values'][1]
    root.clipboard_clear()
    root.clipboard_append(hash_val)
    messagebox.showinfo("Copied", "Hash copied to clipboard")

# ---------- UI ----------
root = tk.Tk()
root.title("SHA-256 Comparator | © Ashutosh Jha")
root.geometry("950x540")
root.configure(bg="#1e1e1e")

# Style
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
    background="#2b2b2b",
    foreground="white",
    rowheight=28,
    fieldbackground="#2b2b2b",
    font=("Segoe UI", 10)
)

style.configure("Treeview.Heading",
    background="#3c3f41",
    foreground="white",
    font=("Segoe UI", 10, "bold")
)

style.map("Treeview", background=[("selected", "#4a90e2")])

# Toolbar
toolbar = tk.Frame(root, bg="#1e1e1e")
toolbar.pack(fill=tk.X, pady=10)

def make_btn(text, cmd):
    return tk.Button(
        toolbar,
        text=text,
        command=cmd,
        bg="#3c3f41",
        fg="white",
        activebackground="#4a90e2",
        activeforeground="white",
        relief="flat",
        padx=12,
        pady=6,
        font=("Segoe UI", 10)
    )

make_btn("Add Files", add_files).pack(side=tk.LEFT, padx=5)
make_btn("Copy Hash", copy_hash).pack(side=tk.LEFT, padx=5)
make_btn("Remove Selected", remove_selected).pack(side=tk.LEFT, padx=5)
make_btn("Clear All", clear_all).pack(side=tk.LEFT, padx=5)

# Table
columns = ("File", "SHA-256", "Status")

tree = ttk.Treeview(root, columns=columns, show="headings", selectmode="extended")
tree.heading("File", text="File")
tree.heading("SHA-256", text="SHA-256")
tree.heading("Status", text="Status")

tree.column("File", width=250)
tree.column("SHA-256", width=520)
tree.column("Status", width=120, anchor="center")

tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Row colors
tree.tag_configure("match", background="#1f3b2d")
tree.tag_configure("mismatch", background="#3b1f1f")

# Footer (copyright)
footer = tk.Label(
    root,
    text="© Ashutosh Jha",
    bg="#1e1e1e",
    fg="#888888",
    font=("Segoe UI", 9)
)
footer.pack(side=tk.BOTTOM, anchor="e", padx=10, pady=5)

# Delete key shortcut
root.bind("<Delete>", lambda e: remove_selected())

root.mainloop()