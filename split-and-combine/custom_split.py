import os
import tkinter as tk
from tkinter import filedialog, messagebox

def split_files(split_directory, split_size):
    if not os.path.isdir(split_directory):
        raise FileNotFoundError("Error: Input is not a directory.")

    for root, dirs, files in os.walk(split_directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_size = os.path.getsize(file_path)
            num_parts = -(-file_size // split_size)  # Ceiling division

            with open(file_path, 'rb') as f:
                for i in range(num_parts):
                    part_file_name = f"{file_path}.part{i:02d}"
                    with open(part_file_name, 'wb') as part_file:
                        part_file.write(f.read(split_size))

            os.remove(file_path)  # Optionally delete the original file
    
    return "Files have been split."

# GUI Application
def select_folder():
    folder = filedialog.askdirectory()
    folder_path_var.set(folder)

def start_splitting():
    split_directory = folder_path_var.get()
    try:
        if not split_directory:
            raise ValueError("Folder path is required.")
        
        split_size = int(split_size_var.get()) * 1024 * 1024  # Convert MB to Bytes
        if split_size <= 0:
            raise ValueError("Split size must be a positive integer.")
        
        message = split_files(split_directory, split_size)
        messagebox.showinfo("Success", message)
    except ValueError as ve:
        messagebox.showerror("Input Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("File Splitter")

# Variables
folder_path_var = tk.StringVar()
split_size_var = tk.StringVar(value="1500")  # Default to 1500MB

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Folder path
tk.Label(frame, text="Folder Path:").grid(row=0, column=0, sticky="e")
tk.Entry(frame, textvariable=folder_path_var, width=40).grid(row=0, column=1)
tk.Button(frame, text="Browse", command=select_folder).grid(row=0, column=2)

# Split size
tk.Label(frame, text="Split Size (MB):").grid(row=1, column=0, sticky="e")
tk.Entry(frame, textvariable=split_size_var, width=10).grid(row=1, column=1, sticky="w")

# Start button
tk.Button(frame, text="Start Splitting", command=start_splitting).grid(row=2, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
