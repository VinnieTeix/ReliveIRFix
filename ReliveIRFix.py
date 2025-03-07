import os
import sys
import winreg
import tkinter as tk
from tkinter import messagebox
import subprocess
import shutil

# Determine base directory
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # Extracted folder in temp
else:
    BASE_DIR = os.path.dirname(__file__)  # Normal script folder

# Paths to the VBS and BAT scripts
VBS_SRC_PATH = os.path.join(BASE_DIR, "Fix_AMD_ReLive_Monitor.vbs")
VBS_DEST_PATH = os.path.join(os.environ["APPDATA"], "Fix_AMD_ReLive_Monitor.vbs")  # Safer location
BAT_PATH = os.path.join(BASE_DIR, "ForceRefresh.bat")

REGISTRY_KEY = "Software\Microsoft\Windows\CurrentVersion\Run"
ENTRY_NAME = "FixReLiveMonitor"

def is_enabled():
    """Check if the startup entry exists."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, ENTRY_NAME)
        return True
    except FileNotFoundError:
        return False

def enable_startup():
    """Enable the startup entry."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, ENTRY_NAME, 0, winreg.REG_SZ, f'wscript.exe "{VBS_DEST_PATH}"')
        messagebox.showinfo("Success", "Startup enabled successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to enable startup: {e}")

def disable_startup():
    """Disable the startup entry."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REGISTRY_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, ENTRY_NAME)
        messagebox.showinfo("Success", "Startup disabled successfully!")
    except FileNotFoundError:
        messagebox.showwarning("Not Found", "Startup entry is already disabled.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to disable startup: {e}")

def run_vbs():
    """Copy the VBS file to a safer location and execute it."""
    try:
        # Copy the VBS file to %APPDATA%
        shutil.copy(VBS_SRC_PATH, VBS_DEST_PATH)  # Copy to AppData
        # Execute the VBS file from AppData
        subprocess.run(["wscript.exe", VBS_DEST_PATH], check=True)
        messagebox.showinfo("Success", "VBS script executed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute VBS: {e}")


def main():
    """Create a simple GUI for enabling/disabling startup."""
    root = tk.Tk()
    root.title("ReLive Startup Manager")
    root.geometry("300x200")

    status_label = tk.Label(root, text=f"Startup Enabled: {is_enabled()}", font=("Arial", 12))
    status_label.pack(pady=10)

    enable_btn = tk.Button(root, text="Enable Startup", command=lambda: [enable_startup(), status_label.config(text=f"Startup Enabled: {is_enabled()}")])
    enable_btn.pack(pady=5)

    disable_btn = tk.Button(root, text="Disable Startup", command=lambda: [disable_startup(), status_label.config(text=f"Startup Enabled: {is_enabled()}")])
    disable_btn.pack(pady=5)

    run_vbs_btn = tk.Button(root, text="Run VBS Script", command=run_vbs)
    run_vbs_btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()