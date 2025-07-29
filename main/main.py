import socket
import os
import platform

computer_name = socket.gethostname()
print("Computer Name:", computer_name)

def find_usb_path_by_label(label):
    system = platform.system()

    if system == "Windows":
        import win32api
        drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
        for drive in drives:
            try:
                volume_name = win32api.GetVolumeInformation(drive)[0]
                if volume_name == label:
                    return drive
            except:
                continue

    elif system == "Linux":
        base_path = f"/media/{os.getlogin()}"
        if os.path.exists(base_path):
            for name in os.listdir(base_path):
                if name == label:
                    return os.path.join(base_path, name)

    elif system == "Darwin":  # macOS
        base_path = "/Volumes"
        for name in os.listdir(base_path):
            if name == label:
                return os.path.join(base_path, name)

    return None

# Example usage
usb_label = "MyPassport"
usb_path = find_usb_path_by_label(usb_label)
print("USB Path:", usb_path)
