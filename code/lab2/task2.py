import os
import argparse

def find_empty_files_and_dirs(path, delete_files=False, delete_dirs=False):
    empty_files = []
    empty_dirs = []

    for root, dirs, files in os.walk(path):
        if not dirs and not files:
            empty_dirs.append(root)
            if delete_dirs:
                try:
                    os.rmdir(root)
                    print(f"Deleted empty directory: {root}")
                except OSError as e:
                    print(f"Error deleting directory {root}: {e}")
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) == 0:
                empty_files.append(file_path)
                if delete_files:
                    try:
                        os.remove(file_path)
                        print(f"Deleted empty file: {file_path}")
                    except OSError as e:
                        print(f"Error deleting file {file_path}: {e}")

    return empty_files, empty_dirs

def main():
    parser = argparse.ArgumentParser(description="Find and delete empty files and directories.")
    parser.add_argument('path', nargs='?', default=os.getcwd(), help="Directory to search")
    parser.add_argument('-d', '--delete-files', action='store_true', help="Delete empty files")
    parser.add_argument('-D', '--delete-dirs', action='store_true', help="Delete empty directories")

    args = parser.parse_args()

    empty_files, empty_dirs = find_empty_files_and_dirs(args.path, args.delete_files, args.delete_dirs)

    if not args.delete_files:
        print("Empty files:")
        for file in empty_files:
            print(file)

    if not args.delete_dirs:
        print("Empty directories:")
        for directory in empty_dirs:
            print(directory)

if __name__ == "__main__":
    main()
