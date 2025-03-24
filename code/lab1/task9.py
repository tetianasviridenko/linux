import platform
import psutil
def get_PC_info():
    info = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Memory": psutil.virtual_memory()
           }
    return info
if __name__ == "__main__":
    PC_info = get_PC_info()
    for key, value in PC_info.items():
        print(f"{key}:{value}")
