import psutil
import argparse
import os

def get_process_info(pid):
    try:
        process = psutil.Process(pid)
        return {
            "pid": pid,
            "exe": process.exe(),
            "cmdline": " ".join(process.cmdline()) if process.cmdline() else ""
        }
    except psutil.NoSuchProcess:
        return None

def list_processes(all_processes):
    if all_processes:
        processes = psutil.process_iter(['pid', 'exe', 'cmdline'])
    else:
        processes = [psutil.Process(os.getpid())]

    for process in processes:
        info = get_process_info(process.pid)
        if info:
            print(f"PID: {info['pid']}, EXE: {info['exe']}, CMDLINE: {info['cmdline']}")

def main():
    parser = argparse.ArgumentParser(description="Show processes info.")
    parser.add_argument('-a', '--all', action='store_true', help="Show all processes info")

    args = parser.parse_args()

    list_processes(args.all)

if __name__ == "__main__":
    main()
