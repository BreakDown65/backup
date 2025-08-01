import socket
import os
from data import adat

print(os.getcwd())
computer_name = socket.gethostname()

def find_usb_path_by_label(label):
    """
    Megmondja, hogy mi egy adott (label) meghajtó elérési útvonala
    """

    import win32api
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
    for drive in drives:
        try:
            volume_name = win32api.GetVolumeInformation(drive)[0]
            if volume_name == label:
                return drive
        except:
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


# mappaCalibre = 'C:/Users/Somoskői Gábor/Backup/Calibre/Job-202410161007548'
mappaObsidianDaily = 'C:/Users/Somoskői Gábor/Backup/Obsidian/ObsidianDaily/Job-202410151128605'
# mappaObsidianWeekly = 'C:/Users/Somoskői Gábor/Backup/Obsidian/ObsidianWeekly/Job-202410151144164'
print("Legfrissebb alkönyvtár:", newest_subdir(adat.SOURCE_SOMOSKOIGABOR["obsidianDaily"]))
