#!/usr/bin/env python3

import subprocess
import platform
import os

LOGO = """
██████╗ ███████╗██████╗ ██████╗ ██╗███████╗ █████╗ 
██╔══██╗██╔════╝██╔══██╗██╔══██╗██║╚════██║██╔══██╗
██████╔╝█████╗  ██████╔╝██████╔╝██║    ██╔╝███████║
██╔══██╗██╔══╝  ██╔═══╝ ██╔══██╗██║   ██╔╝ ██╔══██║
██║  ██║███████╗██║     ██║  ██║██║   ██║  ██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝   ╚═╝  ╚═╝  ╚═╝

███████╗ ██████╗██╗  ██╗███████╗    ██╗    ██╗    ██╗   ██╗ █████╗ 
██╔════╝██╔════╝██║ ██╔╝██╔════╝    ██║    ██║    ╚██╗ ██╔╝██╔══██╗
█████╗  ██║     █████╔╝ ███████╗    ██║ █╗ ██║     ╚████╔╝ ███████║
██╔══╝  ██║     ██╔═██╗ ╚════██║    ██║███╗██║      ╚██╔╝  ██╔══██║
██║     ╚██████╗██║  ██╗███████║    ╚███╔███╔╝       ██║   ██║  ██║
╚═╝      ╚═════╝╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝        ╚═╝   ╚═╝  ╚═╝
"""

def get_os():
    with open("/etc/os-release") as f:
        for line in f:
            if line.startswith("PRETTY_NAME"):
                return line.split("=")[1].strip().strip('"')

def get_kernel():
    return platform.release()

def get_uptime():
    with open("/proc/uptime") as f:
        seconds = float(f.read().split()[0])
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    return f"{h}h {m}m"

def get_cpu():
    with open("/proc/cpuinfo") as f:
        for line in f:
            if "model name" in line:
                return line.split(":")[1].strip()

def get_ram():
    with open("/proc/meminfo") as f:
        lines = f.readlines()
    total = int(lines[0].split()[1]) // 1024
    available = int(lines[2].split()[1]) // 1024
    used = total - available
    return f"{used}MB / {total}MB"

def get_gpu():
    # os.popen запускает терминальную команду и позволяет прочитать её результат
    stream = os.popen("glxinfo | grep 'Device:'")
    output = stream.read()
    
    # Если команда что-то вернула, чистим строку от лишнего
    if output:
        # Разбиваем по двоеточию и берем правую часть, убираем пробелы
        return output.split("Device:")[1].split("(")[0].strip()
    
    return "Unknown GPU"


def get_shell():
    return os.path.basename(os.environ.get("SHELL", "unknown"))

def get_font():
    kitty_conf = os.path.expanduser("~/.config/kitty/kitty.conf")
    if os.path.exists(kitty_conf):
        with open(kitty_conf) as f:
            for line in f:
                if line.startswith("font_family"):
                    return line.split(None, 1)[1].strip()
    else:
        result = subprocess.run(['fc-match', 'monospace'], capture_output=True, text=True)
        return result.stdout.strip().split(':')[0]
print(LOGO)

info = {
    
    "OS":     get_os(),
    "Kernel": get_kernel(),
    "Uptime": get_uptime(),
    "CPU":    get_cpu(),
    "GPU":    get_gpu(),
    "RAM":    get_ram(),
    "Shell":  get_shell(),
    "Font": get_font(),
}


for key, val in info.items():
    print(f"\033[1;34m{key:<10}\033[0m {val}")