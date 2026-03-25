import os
import tkinter as tk
from tkinter import filedialog, messagebox

def split_file(file_path, split_size=1500 * 1024 * 1024):
    file_size = os.path.getsize(file_path)
    num_parts = -(-file_size // split_size)  # Ceiling division

    with open(file_path, 'rb') as f:
        for i in range(num_parts):
            part_file_name = f"{file_path}.part{i:02d}"
            with open(part_file_name, 'wb') as part_file:
                part_file.write(f.read(split_size))

    os.remove(file_path)  # Optionally delete the original file
    return f"File {os.path.basename(file_path)} split into {num_parts} parts."

def split_files_in_directory(split_directory, split_size=1500 * 1024 * 1024):
    if not os.path.isdir(split_directory):
        raise FileNotFoundError("Input is not a directory.")

    for root, _, files in os.walk(split_directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            split_file(file_path, split_size)

    return "All files in the folder have been split."

# GUI Application
def browse():
    selection = selection_var.get()
    if selection == "folder":
        path = filedialog.askdirectory()
    else:
        path = filedialog.askopenfilename()
    path_var.set(path)

def start_splitting():
    selection = selection_var.get()
    path = path_var.get()

    try:
        if not path:
            raise ValueError("Path is required.")

        if selection == "folder":
            message = split_files_in_directory(path)
        else:
            message = split_file(path)

        messagebox.showinfo("Success", message)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create main window
root = tk.Tk()
root.title("File Splitter")

# Variables
selection_var = tk.StringVar(value="folder")
path_var = tk.StringVar()

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Selection type
tk.Label(frame, text="Select:").grid(row=0, column=0, sticky="w")
tk.Radiobutton(frame, text="Folder", variable=selection_var, value="folder").grid(row=0, column=1, sticky="w")
tk.Radiobutton(frame, text="File", variable=selection_var, value="file").grid(row=0, column=2, sticky="w")

# Path input
tk.Label(frame, text="Path:").grid(row=1, column=0, sticky="e")
tk.Entry(frame, textvariable=path_var, width=40).grid(row=1, column=1)
tk.Button(frame, text="Browse", command=browse).grid(row=1, column=2)

# Start button
tk.Button(frame, text="Start Splitting", command=start_splitting).grid(row=2, column=0, columnspan=3, pady=10)

# Run application
root.mainloop()
