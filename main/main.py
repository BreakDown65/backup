import os
import shutil
import socket
from datetime import datetime

# Külső HDD neve
HDD_NAME = "MyPassport"

# Számítógép specifikus mappák
# formátum: gépnév: [(forrás_mappa, cél_almappa), ...]
CONFIG = {
    "Somoskoigabor": [
        (r"C:\Users\Somoskői Gábor\Backup\Calibre\Job-202410161007548", "Backup_Somoskoigabor/calibre"),
        (r"C:\Users\Somoskői Gábor\Backup\Obsidian\ObsidianDaily\Job-202410151128605", "Backup_Somoskoigabor/obsidianDaily"),
        (r"C:\Users\Somoskői Gábor\Backup\Obsidian\ObsidianWeekly\Job-202410151144164", "Backup_Somoskoigabor/obsidianWeekly")
    ],
    "LenovoT530": [
        (r"D:\Work\Reports", "Backup_PC2/Reports"),
        (r"D:\Music", "Backup_PC2/Music"),
    ]
}

def find_external_drive(drive_name):
    """Visszaadja a meghajtó betűjelét a meghajtó neve alapján"""
    from string import ascii_uppercase

    for letter in ascii_uppercase:
        path = f"{letter}:\\"
        if os.path.exists(path):
            try:
                vol_name = os.popen(f"vol {letter}:").read().strip()
                if drive_name.lower() in vol_name.lower():
                    return path
            except:
                continue
    return None


def get_latest_subfolder(path):
    """Visszaadja a legfrissebb almappa elérési útját"""
    if not os.path.exists(path):
        return None

    subfolders = [
        os.path.join(path, d)
        for d in os.listdir(path)
        if os.path.isdir(os.path.join(path, d))
    ]

    if not subfolders:
        return None

    # Rendezés módosítási idő szerint (legfrissebb elől)
    subfolders.sort(key=os.path.getmtime, reverse=True)
    return subfolders[0]

def copy_latest_subfolder(source, dest):
    """Csak a legfrissebb almappát másolja"""
    latest_folder = get_latest_subfolder(source)
    if not latest_folder:
        print(f"❌ Nincs almappa itt: {source}")
        return

    if not os.path.exists(dest):
        os.makedirs(dest)

    folder_name = os.path.basename(latest_folder)
    dest_path = os.path.join(dest, folder_name)

    print(f"📂 Legfrissebb mappa másolása: {latest_folder} -> {dest_path}")
    shutil.copytree(latest_folder, dest_path, dirs_exist_ok=True)

def main():
    hostname = socket.gethostname()
    print(f"💻 Gépnév: {hostname}")

    if hostname not in CONFIG:
        print("❌ Ehhez a géphez nincs konfiguráció!")
        return

    hdd_path = find_external_drive(HDD_NAME)
    if not hdd_path:
        print(f"❌ Külső HDD ({HDD_NAME}) nem található!")
        return

    print(f"✅ Külső HDD elérve: {hdd_path}")

    for src, dst in CONFIG[hostname]:
        dest_path = os.path.join(hdd_path, dst)
        copy_latest_subfolder(src, dest_path)

if __name__ == "__main__":
    main()