import socket
import os
import platform

computer_name = socket.gethostname()

def find_usb_path_by_label(label):
    """
    Különböző operációs rendszerek esetén megmondja,
    hogy mi egy adott (label) meghajtó elérési útvonala
    """
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

def newest_subdir(path):
    """Egy könyvtárban meghatározza a legfrissebb alkönyvtár elérését
    """
    alkonyvtarak = [
        os.path.join(path, d)
        for d in os.listdir(path)
        if os.path.isdir(os.path.join(path, d))
    ]
    
    if not alkonyvtarak:
        return None
    
    # Módosítási idő alapján rendezés
    return max(alkonyvtarak, key=os.path.getmtime)


# Example usage
usb_label = "MyPassport"
usb_path = find_usb_path_by_label(usb_label)
print("USB Path:", usb_path)
print("Computer Name:", computer_name)
print(drives)

mappa = 'C:/Users/Somoskői Gábor/Backup/Calibre/Job-202410161007548'
print("Legfrissebb alkönyvtár:", newest_subdir(mappa))
