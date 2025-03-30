import os
import argparse
import pwd
import grp
import time

def list_directory(wd, show_all, long_format):
    try:
        entries = os.listdir(wd)
    except PermissionError:
        print(f"Permission denied: '{wd}'")
        return

    if not show_all:
        entries = [entry for entry in entries if not entry.startswith('.') or entry in ('.', '..')]

    for entry in sorted(entries):
        full_path = os.path.join(wd, entry)
        if long_format:
            file_info = os.lstat(full_path)
            file_type = 'd' if os.path.isdir(full_path) else '-'
            permissions = ''.join(['r' if file_info.st_mode & 0o400 else '-',
                                   'w' if file_info.st_mode & 0o200 else '-',
                                   'x' if file_info.st_mode & 0o100 else '-',
                                   'r' if file_info.st_mode & 0o040 else '-',
                                   'w' if file_info.st_mode & 0o020 else '-',
                                   'x' if file_info.st_mode & 0o010 else '-',
                                   'r' if file_info.st_mode & 0o004 else '-',
                                   'w' if file_info.st_mode & 0o002 else '-',
                                   'x' if file_info.st_mode & 0o001 else '-'])
            owner = pwd.getpwuid(file_info.st_uid).pw_name
            group = grp.getgrgid(file_info.st_gid).gr_name
            hard_links = file_info.st_nlink
            size = file_info.st_size
            mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_info.st_mtime))
            print(f"{file_type}{permissions} {owner} {group} {hard_links} {size} {mod_time} {entry}")
        else:
            print(entry)

def main():
    parser = argparse.ArgumentParser(description="List directory contents.")
    parser.add_argument('wd', nargs='?', default=os.getcwd(), help="Working directory")
    parser.add_argument('-l', '--long', action='store_true', help="Show detailed information")
    parser.add_argument('-a', '--all', action='store_true', help="Show all files including hidden")

    args = parser.parse_args()

    list_directory(args.wd, args.all, args.long)

if __name__ == "__main__":
    main()

