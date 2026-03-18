import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog

LOG_FILE = "undo_log.json"

TYPES = {
    "Images": (".jpg", ".jpeg", ".png"),
    "PDFs": (".pdf",),
    "Audio": (".mp3", ".wav"),
    "Videos": (".mp4", ".mkv")
}

# ------------------- Organizer -------------------
def organize(folder):
    undo_data = []

    for name in os.listdir(folder):
        src = os.path.join(folder, name)

        if os.path.isdir(src):
            continue

        for category, exts in TYPES.items():
            if name.lower().endswith(exts):
                dst_dir = os.path.join(folder, category)
                os.makedirs(dst_dir, exist_ok=True)
                dst = os.path.join(dst_dir, name)
                shutil.move(src, dst)
                undo_data.append((dst, src))
                break
        else:
            dst_dir = os.path.join(folder, "Others")
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(dst_dir, name)
            shutil.move(src, dst)
            undo_data.append((dst, src))

    with open(LOG_FILE, "w") as f:
        json.dump(undo_data, f)

# ------------------- Undo -------------------
def undo():
    if not os.path.exists(LOG_FILE):
        print("Nothing to undo")
        return

    with open(LOG_FILE, "r") as f:
        moves = json.load(f)

    for src, dst in moves:
        if os.path.exists(src):
            shutil.move(src, dst)

    os.remove(LOG_FILE)
    print("Undo completed")

# ------------------- Folder Picker -------------------
def get_folder():
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder = filedialog.askdirectory(title="Select folder to organize")
        root.destroy()
        return folder
    except Exception as e:
        print("Error opening folder picker:", e)
        return None

# ------------------- Main -------------------
def main():
    choice = input("o = organize | u = undo : ").lower()

    if choice == "o":
        folder = get_folder()
        if not folder:
            print("No folder selected. Exiting.")
            return
        organize(folder)
        print("Organized:", folder)

    elif choice == "u":
        undo()

    else:
        print("Invalid choice. Use 'o' to organize or 'u' to undo.")

if __name__ == "__main__":
    main()
