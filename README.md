# Tools

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/ikmalghani/tools)

A collection of personal Python utility scripts designed for various file management and automation tasks. Each tool is self-contained within its respective directory.

## Tools Included

- [Git Size Guard](#git-size-guard)
- [TV Series File Renamer](#tv-series-file-renamer)
- [Softcode Subtitles](#softcode-subtitles)
- [File Splitter & Combiner](#file-splitter--combiner)

---

### Git Size Guard

A set of scripts to help manage and prevent large files from being committed to a Git repository, which often has file size limits.

#### `size_checker.py`
This script scans a specified directory and its subdirectories to find and report any files that exceed a size limit (default 90MB). It's useful as a pre-commit check to avoid accidentally attempting to push oversized files.

**Usage:**
Run the script from your terminal and provide the directory path when prompted.
```bash
python git-size-guard/size_checker.py
```

#### `extract_100mb.py`
This script scans a directory for files larger than 100MB, moves them to a specified destination folder, and creates a log of the moved files. This helps in separating large assets from a Git repository before a commit.

**Usage:**
Run the script from your terminal. It will prompt for the source and destination directories.
```bash
python git-size-guard/extract_100mb.py
```

---

### TV Series File Renamer

A GUI-based tool for batch renaming TV series episode files into a clean, consistent format.

#### `rename_files.py`
This script launches a graphical interface that allows you to:
- Select a folder containing your episode files.
- Specify a new series name and other metadata like resolution, source, and release group.
- The script automatically detects season/episode numbers from common formats (e.g., `S01E02`, `E02`, `02`) and renames the files.

**Usage:**
Running the script opens the GUI application.
```bash
python rename-files/rename_files.py
```

---

### Softcode Subtitles

A GUI-based tool to embed subtitle files into video files as a selectable track (soft subtitles). This process is fast as it copies the existing video and audio streams without re-encoding.

#### `softcode_subs.py`
This script launches a graphical interface to process an entire directory. It automatically matches video files (`.mkv`, `.mp4`) with corresponding subtitle files (`.srt`, `.ass`) based on naming conventions for movies and TV shows. It uses FFmpeg to create new `.mp4` video files with the embedded, selectable subtitles.

**Dependencies:**
- **FFmpeg:** You must have FFmpeg installed and accessible in your system's PATH.

**Usage:**
Run the script to launch the GUI. Select the directory containing your video and subtitle files to begin processing.
```bash
python softcode-subs/softcode_subs.py
```

---

### File Splitter & Combiner

A collection of GUI tools to split large files into smaller, more manageable parts and to combine those parts back into the original file. This is useful for circumventing file size limits on cloud storage or transfer services.

#### `split.py` / `custom_split.py`
GUI tools to split files into smaller chunks.
- `split.py`: Splits a single file or all files in a folder into 1500MB parts.
- `custom_split.py`: Splits all files in a folder into parts of a user-defined size (in MB).

After splitting, the original files are deleted.

**Usage:**
```bash
# For a fixed 1500MB split size
python split-and-combine/split.py

# For a custom split size
python split-and-combine/custom_split.py
```

#### `combine.py`
A GUI tool that reverses the splitting process. It scans a directory for file parts (e.g., `file.part00`, `file.part01`), combines them into the original single file, and removes the part files upon completion.

**Usage:**
Run the script to launch the GUI, then select the directory containing the file parts.
```bash
python split-and-combine/combine.py
