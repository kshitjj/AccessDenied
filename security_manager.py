import os
import subprocess
import platform
import ctypes
import winreg

# 1. Disabling USB ports
def disable_usb_ports():
    key_path = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
    try:
        # using the winreg change the value in window registry
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, "Start", 0, winreg.REG_DWORD, 4)  # Changing usbstor to 4 disables the USB ports
        winreg.CloseKey(reg_key)
        print("USB ports disabled")
    except Exception as e:
        print("Error:", e)

# 2. Disable Bluetooth
def disable_bluetooth():
    try:
        # first we search for Pnpdevices which has bluetooth in it's name
        # get name for the device and disable it.
        command = "powershell -command \"Get-PnpDevice | Where-Object {$_.Friendlyname -like 'bluetooth'} | Disable-PnpDevice -Confirm:$false\""
        os.system(command)
        print("Bluetooth disabled")
    except Exception as e:
        print("Error:", e)

# 3. Restrict command prompt
def disable_command_prompt():
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(9, 1, 0, ctypes.byref(ctypes.c_bool()))
        os.system("reg add HKCU\Software\Policies\Microsoft\Windows\System /v DisableCMD /t REG_DWORD /d 1 /f")
        print("Command Prompt disabled.")
    except Exception as e:
        print("Error:", e)

# 4. Check and Block Website
def block_website(website):
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"

    # Redirect ip which won't work, we can put anything here.
    redirect_ip = "127.0.0.1"

    # Search for host file
    if not os.path.isfile(hosts_path):
        print("Hosts file not found.")
        return

    # Check for permissions
    if not os.access(hosts_path, os.W_OK):
        print("Permission denied. Run the script as an administrator.")
        return

    # open the host file
    with open(hosts_path, "r") as hosts_file:
        content = hosts_file.read()

    # check if the website is present in host file
    if website in content:
        print(f"{website} is already blocked.")
        return

    # write the website and redirect to localhost/127.0.0.1
    with open(hosts_path, "a") as hosts_file:
        hosts_file.write(f"\n{redirect_ip} {website}")
        print(f"{website} blocked successfully.")

def flush_dns_cache():
    # clearing the dns cache doesn't allow user to access the website even if they 
    # have been to the website before
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
