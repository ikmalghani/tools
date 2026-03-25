import os

def scan_folder(base_dir, limit_mb=90):
    limit_bytes = limit_mb * 1024 * 1024
    folder_count = 0
    big_file_count = 0
    total_big_size = 0
    dirs_with_big_files = []

    for root, dirs, files in os.walk(base_dir):
        folder_count += 1
        print(f"[✓] Checking {root}...")

        big_files = []
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
            except OSError:
                continue  # skip unreadable files
            if size > limit_bytes:
                size_mb = size / (1024 * 1024)
                big_files.append((file, size_mb))
                big_file_count += 1
                total_big_size += size_mb

        if not big_files:
            print(f"    No file exceed {limit_mb} MB found in {root}")
        else:
            print("    Large files found:")
            for file, size_mb in big_files:
                print(f"    {file} → {size_mb:.2f} MB")
            dirs_with_big_files.append(root)

        print()  # blank line after each folder

    # Summary
    print("===== SUMMARY =====")
    print(f"Total folders checked : {folder_count}")
    print(f"Total large files     : {big_file_count}")
    print(f"Total large size      : {total_big_size:.2f} MB")

    if dirs_with_big_files:
        print("\nDirectories with files > "
              f"{limit_mb} MB:")
        for d in dirs_with_big_files:
            print(f" - {d}")
    else:
        print("\nNo directories contained files > "
              f"{limit_mb} MB")


if __name__ == "__main__":
    base_dir = input("Enter directory to scan: ").strip()
    if not os.path.isdir(base_dir):
        print("Directory not found!")
    else:
        scan_folder(base_dir)
