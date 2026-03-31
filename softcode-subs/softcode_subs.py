import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def softcode_subtitles(video_file, subtitle_files, output_file):
    if not output_file.lower().endswith(".mp4"):
        raise ValueError("Output file must have a .mp4 extension for this script.")

    # Use FFmpeg to softcode the subtitles
    cmd = ["ffmpeg", "-i", video_file]
    map_args = ["-map", "0:v:0", "-map", "0:a:0"]
    input_index = 1
    for sub in subtitle_files:
        cmd.extend(["-i", sub])
        map_args.extend(["-map", f"{input_index}:0"])
        input_index += 1
    
    cmd.extend(map_args)
    cmd.extend(["-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", output_file])
    
    subprocess.run(cmd, check=True)
    
    subs_str = ", ".join(os.path.basename(s) for s in subtitle_files)
    return f"Processed: {video_file} with {subs_str}\nOutput saved to: {output_file}"

def find_video_and_subtitle_files(directory):
    """Find video and subtitle files in the given directory and subdirectories"""
    video_extensions = ['.mkv', '.mp4', '.avi']
    subtitle_extensions = ['.srt', '.ass']
    
    video_files = []
    subtitle_files = []
    
    for root_dir, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root_dir, file)
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in video_extensions:
                video_files.append(file_path)
            elif file_ext in subtitle_extensions:
                subtitle_files.append(file_path)
    
    return video_files, subtitle_files

def extract_episode_info(filename):
    """Extract episode information from filename for better matching"""
    # Remove extension
    name = os.path.splitext(filename)[0]
    
    # Look for common episode patterns
    import re
    
    # Pattern 1: E01, E02, etc.
    episode_match = re.search(r'[Ee](\d{1,2})', name)
    if episode_match:
        episode_num = episode_match.group(1)
        # Extract series name (everything before the episode)
        series_part = name[:episode_match.start()].strip('. ')
        return series_part, episode_num
    
    # Pattern 2: Episode 01, Episode 02, etc.
    episode_match = re.search(r'[Ee]pisode\s*(\d{1,2})', name)
    if episode_match:
        episode_num = episode_match.group(1)
        series_part = name[:episode_match.start()].strip('. ')
        return series_part, episode_num
    
    # Pattern 3: S01E01, S02E01, etc.
    episode_match = re.search(r'[Ss](\d{1,2})[Ee](\d{1,2})', name)
    if episode_match:
        season_num = episode_match.group(1)
        episode_num = episode_match.group(2)
        series_part = name[:episode_match.start()].strip('. ')
        return f"{series_part} S{season_num}", episode_num
    
    # If no pattern found, return the filename as is
    return name, ""

def process_directory():
    directory = directory_var.get()
    if not directory:
        messagebox.showerror("Error", "Please select a directory first.")
        return
    
    try:
        video_files, subtitle_files = find_video_and_subtitle_files(directory)
        
        if not video_files:
            messagebox.showerror("Error", "No video files found in the selected directory.")
            return
        
        if not subtitle_files:
            messagebox.showerror("Error", "No subtitle files found in the selected directory.")
            return
        
        # Process each video file with available subtitle files
        results = []
        results.append(f"Found {len(video_files)} video files and {len(subtitle_files)} subtitle files")
        for video_file in video_files:
            video_dir = os.path.dirname(video_file)
            video_name = os.path.basename(video_file)
            video_series, video_episode = extract_episode_info(video_name)
            video_name_no_ext = os.path.splitext(video_name)[0]
            
            matching_subtitles = []
            
            for subtitle_file in subtitle_files:
                sub_dir = os.path.dirname(subtitle_file)
                sub_name = os.path.basename(subtitle_file)
                
                # Same directory matching
                if sub_dir == video_dir:
                    if video_episode:
                        # TV Episode: check episode match
                        sub_series, sub_episode = extract_episode_info(sub_name)
                        if video_episode == sub_episode:
                            matching_subtitles.append(subtitle_file)
                    else:
                        # Movie: exact name match
                        if video_name_no_ext.lower() == os.path.splitext(sub_name)[0].lower():
                            matching_subtitles.append(subtitle_file)
                
                # Folder matching: if sub is in a subdir path that contains a folder matching the episode
                elif sub_dir.startswith(video_dir + os.sep) and video_episode:
                    rel_path = os.path.relpath(sub_dir, video_dir)
                    path_parts = rel_path.split(os.sep)
                    match = False
                    for part in path_parts:
                        folder_series, folder_episode = extract_episode_info(part)
                        if folder_episode == video_episode:
                            match = True
                            break
                    if match:
                        matching_subtitles.append(subtitle_file)
            
            if matching_subtitles:
                # Create output filename in the video's directory
                output_file = os.path.join(video_dir, f"[Eng Subbed] {video_name_no_ext}.mp4")
                
                try:
                    message = softcode_subtitles(video_file, matching_subtitles, output_file)
                    results.append(f"✓ {message}")
                except Exception as e:
                    results.append(f"✗ Failed to process {video_name}: {str(e)}")
            else:
                results.append(f"⚠ No matching subtitle found for {video_name} (Episode {video_episode})")
        
        # Show results
        result_text = "\n".join(results)
        messagebox.showinfo("Processing Complete", result_text)
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_directory():
    directory = filedialog.askdirectory()
    directory_var.set(directory)

# Create the main window
root = tk.Tk()
root.title("Softcode Subtitles - Directory Mode")

# Variables
directory_var = tk.StringVar()

# Layout
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Directory selection
tk.Label(frame, text="Directory:").grid(row=0, column=0, sticky="e")
tk.Entry(frame, textvariable=directory_var, width=50).grid(row=0, column=1)
tk.Button(frame, text="Browse", command=select_directory).grid(row=0, column=2)

# Process button
tk.Button(frame, text="Process All Files", command=process_directory).grid(row=1, column=0, columnspan=3, pady=20)

# Instructions
instructions = tk.Label(frame, text="Select a directory containing video and subtitle files.\nThe script will automatically match files by name and process them.", 
                      justify="center", fg="blue")
instructions.grid(row=2, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
