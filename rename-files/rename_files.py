import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to rename files
def rename_files(folder_path, new_name, resolution, source, group_name, extension):
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"The folder path {folder_path} does not exist.")

    files = os.listdir(folder_path)
    
    # Patterns to match different episode number formats
    pattern_s_e = re.compile(r"S(\d{2})E(\d{2})", re.IGNORECASE)
    pattern_e = re.compile(r"E(\d{2})", re.IGNORECASE)
    pattern_num = re.compile(r"(\d{2})")

    for file in files:
        file_name, file_extension = os.path.splitext(file)
        season_episode = None

        match_s_e = pattern_s_e.search(file_name)
        if match_s_e:
            season_episode = f"S{match_s_e.group(1)}E{match_s_e.group(2)}"
        elif pattern_e.search(file_name):
            season_episode = f"E{pattern_e.search(file_name).group(1)}"
        elif pattern_num.search(file_name):
            season_episode = pattern_num.search(file_name).group(1)

        if season_episode:
            new_file_name = f"{new_name}.{season_episode}"
            if resolution:
                new_file_name += f".{resolution}"
            if source:
                new_file_name += f".{source}"
            if group_name:
                new_file_name += f"-{group_name}"
            new_file_name += f".{extension}"

            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, new_file_name)

            os.rename(old_file_path, new_file_path)
            print(f"Renamed: {file} -> {new_file_name}")
        else:
            print(f"Skipping: {file} (No match for season/episode formats)")

# GUI Application
def select_folder():
    folder = filedialog.askdirectory()
    folder_path_var.set(folder)

def start_renaming():
    folder_path = folder_path_var.get()
    new_name = new_name_var.get()
    resolution = resolution_var.get()
    source = source_var.get()
    group_name = group_name_var.get()
    extension = extension_var.get()

    if not folder_path or not new_name or not extension:
        messagebox.showerror("Error", "Please fill in all required fields (Folder Path, New Name, Extension).")
        return

    try:
        rename_files(folder_path, new_name, resolution, source, group_name, extension)
        messagebox.showinfo("Success", "Files renamed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("TV Series File Renamer")

# Variables
folder_path_var = tk.StringVar()
new_name_var = tk.StringVar()
resolution_var = tk.StringVar()
source_var = tk.StringVar()
group_name_var = tk.StringVar()
extension_var = tk.StringVar()

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Folder path
tk.Label(frame, text="Folder Path:").grid(row=0, column=0, sticky="e")
tk.Entry(frame, textvariable=folder_path_var, width=40).grid(row=0, column=1)
tk.Button(frame, text="Browse", command=select_folder).grid(row=0, column=2)

# New name
tk.Label(frame, text="New Name:").grid(row=1, column=0, sticky="e")
tk.Entry(frame, textvariable=new_name_var, width=40).grid(row=1, column=1, columnspan=2)

# Resolution
tk.Label(frame, text="Resolution:").grid(row=2, column=0, sticky="e")
tk.Entry(frame, textvariable=resolution_var, width=40).grid(row=2, column=1, columnspan=2)

# Source
tk.Label(frame, text="Source:").grid(row=3, column=0, sticky="e")
tk.Entry(frame, textvariable=source_var, width=40).grid(row=3, column=1, columnspan=2)

# Group name
tk.Label(frame, text="Group Name:").grid(row=4, column=0, sticky="e")
tk.Entry(frame, textvariable=group_name_var, width=40).grid(row=4, column=1, columnspan=2)

# Extension
tk.Label(frame, text="Extension:").grid(row=5, column=0, sticky="e")
tk.Entry(frame, textvariable=extension_var, width=40).grid(row=5, column=1, columnspan=2)

# Start button
tk.Button(frame, text="Start Renaming", command=start_renaming).grid(row=6, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
