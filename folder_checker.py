import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from collections import defaultdict

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes / (1024**2):.2f} MB"
    else:
        return f"{size_bytes / (1024**3):.2f} GB"

def analyze_folder(folder_path):
    file_stats = defaultdict(lambda: {"count": 0, "size": 0})
    total_files = 0
    total_size = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            total_files += 1
            path = os.path.join(root, file)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            ext = os.path.splitext(file)[1].lower() or "(bez rozszerzenia)"
            file_stats[ext]["count"] += 1
            file_stats[ext]["size"] += size
            total_size += size

    return file_stats, total_files, total_size

def choose_folder():
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    tree.delete(*tree.get_children())
    file_stats, total_files, total_size = analyze_folder(folder_path)

    for ext, data in sorted(file_stats.items(), key=lambda x: -x[1]["size"]):
        tree.insert("", "end", values=(ext, data["count"], format_size(data["size"])))

    total_label.config(text=f"Łącznie plików: {total_files} | Łączny rozmiar: {format_size(total_size)}")

# --- GUI ---
root = tk.Tk()
root.title("Analiza folderu")
root.geometry("600x400")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

ttk.Button(frame, text="Wybierz folder", command=choose_folder).pack(pady=5)

columns = ("Rozszerzenie", "Liczba plików", "Łączny rozmiar")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.pack(fill="both", expand=True)

total_label = ttk.Label(frame, text="Brak danych")
total_label.pack(pady=5)

root.mainloop()
