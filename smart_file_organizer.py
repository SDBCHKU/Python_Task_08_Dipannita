import os
import shutil
from collections import Counter
from datetime import datetime

# File categories
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"],
    "Programs": [".exe", ".msi"]
}

# -------------------------------
# Module 1: Directory Selection
# -------------------------------
def get_directory():
    path = input("Enter Folder Path: ")
    if not os.path.exists(path):
        print("Invalid folder path!")
        return None
    return path


# -------------------------------
# Module 2: File Scanning
# -------------------------------
def scan_files(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    print(f"\nTotal Files Found: {len(files)}")
    for file in files:
        print(file)
    
    return files


# -------------------------------
# Module 3: File Organization
# -------------------------------
def organize_files(path, files):
    for file in files:
        file_ext = os.path.splitext(file)[1].lower()
        moved = False

        for folder, extensions in FILE_TYPES.items():
            if file_ext in extensions:
                dest = os.path.join(path, folder)
                os.makedirs(dest, exist_ok=True)
                shutil.move(os.path.join(path, file), os.path.join(dest, file))
                moved = True
                break

        if not moved:
            other_folder = os.path.join(path, "Others")
            os.makedirs(other_folder, exist_ok=True)
            shutil.move(os.path.join(path, file), os.path.join(other_folder, file))


# -------------------------------
# Module 4: Statistics
# -------------------------------
def file_statistics(path):
    stats = Counter()

    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)
        if os.path.isdir(folder_path):
            stats[folder] = len(os.listdir(folder_path))

    print("\n--- File Statistics ---")
    for key, value in stats.items():
        print(f"{key}: {value}")

    return stats


# -------------------------------
# Module 5: Search
# -------------------------------
def search_files(path):
    search = input("\nEnter file name or extension to search: ")
    results = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if search.lower() in file.lower():
                results.append(file)

    if results:
        print("\nSearch Results:")
        for r in results:
            print(r)
    else:
        print("No files found.")


# -------------------------------
# Module 6: Duplicate Detection
# -------------------------------
def find_duplicates(files):
    duplicates = [item for item, count in Counter(files).items() if count > 1]

    print("\n--- Duplicate Files ---")
    if duplicates:
        for d in duplicates:
            print(d)
    else:
        print("No Duplicate Files Found")

    return duplicates


# -------------------------------
# Module 7: Report Generation
# -------------------------------
def generate_report(path, stats, duplicates):
    report_file = os.path.join(path, "file_report.txt")

    with open(report_file, "w") as f:
        f.write("FILE ORGANIZER REPORT\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Folder: {path}\n\n")

        f.write("Statistics:\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")

        f.write("\nDuplicate Files:\n")
        if duplicates:
            for d in duplicates:
                f.write(d + "\n")
        else:
            f.write("No duplicates found\n")

    print("\nReport Generated: file_report.txt")


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def main():
    path = get_directory()
    if not path:
        return

    files = scan_files(path)
    find_duplicates(files)
    organize_files(path, files)
    stats = file_statistics(path)
    search_files(path)
    generate_report(path, stats, files)


if __name__ == "__main__":
    main()