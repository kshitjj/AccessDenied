import os
import subprocess
import platform
import ctypes
import winreg

# 1. Interacting with the Windows Registry Editor
# Here, we'll modify a registry key to disable USB ports.
def disable_usb_ports():
    key_path = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "Start", 0, winreg.REG_DWORD, 4)  # Changing usbstor to 4 disables the USB ports
        winreg.CloseKey(reg_key)
        print("USB ports disabled")
    except Exception as e:
        print("Error:", e)

# 2. Implementing security measures
# Disable Bluetooth
def disable_bluetooth():
    try:
        command = "powershell -command \"Get-PnpDevice | Where-Object {$_.Friendlyname -like 'bluetooth'} | Disable-PnpDevice -Confirm:$false\""
        os.system(command)
        print("Bluetooth disabled")
    except Exception as e:
        print("Error:", e)

# Restrict command prompt
def disable_command_prompt():
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(9, 1, 0, ctypes.byref(ctypes.c_bool()))
        os.system("reg add HKCU\Software\Policies\Microsoft\Windows\System /v DisableCMD /t REG_DWORD /d 1 /f")
        print("Command Prompt disabled.")
    except Exception as e:
        print("Error:", e)

# Block Website
def block_website(website):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    redirect_ip = "127.0.0.1"

    if not os.path.isfile(hosts_path):
        print("Hosts file not found.")
        return

    if not os.access(hosts_path, os.W_OK):
        print("Permission denied. Run the script as an administrator.")
        return

    with open(hosts_path, "r") as hosts_file:
        content = hosts_file.read()

    if website in content:
        print(f"{website} is already blocked.")
        return

    with open(hosts_path, "a") as hosts_file:
        hosts_file.write(f"\n{redirect_ip} {website}")
        print(f"{website} blocked successfully.")

def flush_dns_cache():
    system = platform.system()
    if system == "Windows":
        try:
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, check=True)
            print("DNS cache flushed successfully.")
        except subprocess.CalledProcessError as e:
            print("Error flushing DNS cache:", e)
    else:
        print("DNS cache flushing is not supported on this platform.")

# Main program
if __name__ == "__main__":
    disable_usb_ports()
    disable_bluetooth()
    disable_command_prompt()
    block_website("facebook.com")
    block_website("www.facebook.com")
    flush_dns_cache()
    input("Press Enter to continue...")
