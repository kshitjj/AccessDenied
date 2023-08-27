import os
import ctypes
import winreg

# 1. Enabling USB ports
def enable_usb_ports():
    key = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "Start", 0, winreg.REG_DWORD, 3)  
        # value "3" re-enables the usb ports, but doesn't remove existing usb.
        winreg.CloseKey(reg_key)
        print("USB ports enabled.")
    except Exception as e:
        print("Error:", e)

# 2. Enabling Bluetooth
def enable_bluetooth():
    try:
        # command gets bluetooth and disables it.
        command = "powershell -command \"Get-PnpDevice | Where-Object {$_.Friendlyname -like 'Bluetooth'} | Enable-PnpDevice -Confirm:$false\""
        os.system(command)
        print("Bluetooth enabled")
    except Exception as e:
        print("Error:", e)

# 3. Allow command prompt
def enable_command_prompt():
    try:
        # the line below checks for level of privelege we have over the system.
        ctypes.windll.ntdll.RtlAdjustPrivilege(9, 1, 0, ctypes.byref(ctypes.c_bool()))
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Policies\\Microsoft\\Windows\\System", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, "DisableCMD", 0, winreg.REG_DWORD, 0) # value "0" enables the command prompt
        winreg.CloseKey(reg_key)
        print("Command Prompt disabled.")
    except Exception as e:
        print("Error:", e)


# 4. Unblocking access to a specific website
def unblock_website(website):
    try:
        hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
        # searches and removes lines containing "website"
        with open(hosts_path, "r+") as hosts_file:
            lines = hosts_file.readlines()
            hosts_file.seek(0)
            for line in lines:
                if not line.startswith(f"127.0.0.1 {website}"):
                    hosts_file.write(line)
            # truncate resizes the file, as we have removed some lines from it.
            hosts_file.truncate()
        print(f"Access to {website} unblocked.")
    except Exception as e:
        print("Error:", e)

# Main program
if __name__ == "__main__":
    enable_usb_ports()
    enable_bluetooth()
    enable_command_prompt()
    unblock_website("facebook.com")
    unblock_website("www.facebook.com")
    input("Press Enter to continue...")
