import os
import platform

def get_uptime():
    system = platform.system()
    if system == "Linux":
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
    elif system == "Windows":
        import ctypes
        from ctypes import wintypes, windll

        class Uptime(ctypes.Structure):
            _fields_ = [("IdleTime", wintypes.LARGE_INTEGER),
                        ("TickCount", wintypes.LARGE_INTEGER)]
        lib = windll.kernel32
        uptime = wintypes.DWORD()
        lib.GetTickCount64.restype = wintypes.ULONGLONG
        ms = lib.GetTickCount64()
        return ms / 1000.0
    elif system == "Darwin":
        import subprocess
        output = subprocess.check_output("sysctl -n kern.boottime", shell=True).decode()
        import re, time
        match = re.search(r'{ sec = (\d+),', output)
        if match:
            boot_time = int(match.group(1))
            return time.time() - boot_time
        else:
            return None
    else:
        return None

if __name__ == "__main__":
    uptime_seconds = get_uptime()
    if uptime_seconds is not None:
        print(f"System uptime: {uptime_seconds:.2f} seconds")
    else:
        print("Could not determine uptime for this OS.")
