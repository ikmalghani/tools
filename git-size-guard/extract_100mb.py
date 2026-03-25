import os
import shutil

# Define the size threshold (100MB)
SIZE_THRESHOLD = 100 * 1024 * 1024  # 100MB in bytes


def move_large_files(start_path, destination_dir, log_path):
    moved_files = []
    for root, _, files in os.walk(start_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.getsize(file_path) > SIZE_THRESHOLD:
                    dest_path = os.path.join(destination_dir, file)
                    print(f"Moving: {file_path} -> {dest_path}")
                    shutil.move(file_path, dest_path)
                    moved_files.append(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    with open(log_path, "w", encoding="utf-8") as log_file:
        for path in moved_files:
            log_file.write(path + "\n")


if __name__ == "__main__":
    start_path = input("Enter the folder path to scan: ").strip()
    destination_dir = input("Enter the destination folder for files >100MB: ").strip()

    if not start_path:
        start_path = os.getcwd()

    if not destination_dir:
        destination_dir = os.path.join(os.getcwd(), "large_files")

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir, exist_ok=True)

    log_path = os.path.join(destination_dir, "moved_files.log")
    move_large_files(start_path, destination_dir, log_path)
