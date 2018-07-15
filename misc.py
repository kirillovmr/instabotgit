import sys

def platform():
    return sys.platform.lower()

def python_version():
    if "darwin" in platform() or "linux" in platform():
        return "python3"
    elif "win32" in platform():
        return "python"
