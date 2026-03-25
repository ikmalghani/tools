import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def softcode_subtitles(video_file, subtitle_file, output_file):
    if not output_file.lower().endswith(".mp4"):
        raise ValueError("Output file must have a .mp4 extension for this script.")

    # Use FFmpeg to softcode the subtitles
    # -map 0:v:0 maps the first video stream from input 0 (video file)
    # -map 0:a:0 maps the first audio stream from input 0 (video file)
    # -map 1:0 maps the first subtitle stream from input 1 (subtitle file)
    # This ensures we use the external subtitle file, not existing ones
    subprocess.run([
        "ffmpeg",
        "-i", video_file,
        "-i", subtitle_file,
        "-map", "0:v:0",        # Map video from first input (video file)
        "-map", "0:a:0",        # Map audio from first input (video file)
        "-map", "1:0",          # Map subtitle from second input (subtitle file)
        "-c:v", "copy",         # Copy video without re-encoding
        "-c:a", "copy",         # Copy audio without re-encoding
        "-c:s", "mov_text",     # Convert SRT to mov_text (MP4-compatible)
        output_file
    ], check=True)

    return f"Processed: {video_file} with {subtitle_file}\nOutput saved to: {output_file}"

def find_video_and_subtitle_files(directory):
    """Find video and subtitle files in the given directory"""
    video_extensions = ['.mkv', '.mp4', '.avi']
    subtitle_extensions = ['.srt', '.ass']
    
    video_files = []
    subtitle_files = []
    
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
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
        for video_file in video_files:
            video_name = os.path.basename(video_file)
            video_series, video_episode = extract_episode_info(video_name)
            video_name_no_ext = os.path.splitext(video_name)[0]
            
            matching_subtitle = None
            
            # Check if this is a TV episode (has episode info) or a movie (no episode info)
            if video_episode:
                # TV Episode logic: Find matching subtitle file using episode info
                best_match_score = 0
                
                for subtitle_file in subtitle_files:
                    subtitle_name = os.path.basename(subtitle_file)
                    subtitle_series, subtitle_episode = extract_episode_info(subtitle_name)
                    
                    # Calculate match score
                    match_score = 0
                    
                    # Episode number must match exactly
                    if video_episode == subtitle_episode and video_episode:
                        match_score += 10
                        
                        # Series name similarity (case-insensitive)
                        if video_series.lower() == subtitle_series.lower():
                            match_score += 5
                        elif video_series.lower() in subtitle_series.lower() or subtitle_series.lower() in video_series.lower():
                            match_score += 3
                        
                        # Additional points for common patterns
                        if any(pattern in video_name.lower() and pattern in subtitle_name.lower() 
                               for pattern in ['shark', 'storm', 'phanteam']):
                            match_score += 2
                    
                    if match_score > best_match_score:
                        best_match_score = match_score
                        matching_subtitle = subtitle_file
                
                # Only process if we found a match with episode score >= 10
                if matching_subtitle and best_match_score >= 10:
                    # Create output filename
                    output_file = os.path.join(directory, f"[Eng Subbed] {video_name_no_ext}.mp4")
                    
                    try:
                        message = softcode_subtitles(video_file, matching_subtitle, output_file)
                        results.append(f"✓ {message}")
                    except Exception as e:
                        results.append(f"✗ Failed to process {video_name}: {str(e)}")
                else:
                    results.append(f"⚠ No matching subtitle found for {video_name} (Episode {video_episode})")
            else:
                # Movie logic: Find subtitle with exact same name (case-insensitive, without extension)
                for subtitle_file in subtitle_files:
                    subtitle_name = os.path.basename(subtitle_file)
                    subtitle_name_no_ext = os.path.splitext(subtitle_name)[0]
                    
                    # Check for exact match (case-insensitive)
                    if video_name_no_ext.lower() == subtitle_name_no_ext.lower():
                        matching_subtitle = subtitle_file
                        break
                
                if matching_subtitle:
                    # Create output filename
                    output_file = os.path.join(directory, f"[Eng Subbed] {video_name_no_ext}.mp4")
                    
                    try:
                        message = softcode_subtitles(video_file, matching_subtitle, output_file)
                        results.append(f"✓ {message}")
                    except Exception as e:
                        results.append(f"✗ Failed to process {video_name}: {str(e)}")
                else:
                    results.append(f"⚠ No matching subtitle found for {video_name} (Movie - exact name match required)")
        
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
