import os
import csv


def export_modlist(mods, dir: str):
    with open(os.path.join(dir, 'modlist.csv'), 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["name", "source", "authors"])  # Row at the top for info
        for mod in mods:
            writer.writerow([mod.name, mod.source, mod.authors])


def import_modlist(mods, file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            modlist = list(csv.DictReader(file))
        for i in modlist:
            print(i)
        return modlist
    except FileNotFoundError:
        return False
