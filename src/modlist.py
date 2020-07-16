import json

def export_modlist(mods):
    mods_json = []
    for mod in mods:
        mod_json = {"name": mod.name, "source": mod.source, "authors": mod.authors}
        mods_json.append(mod_json)
    with open('modlist.json', 'w', encoding='utf-8') as json_file:
        json.dump(mods_json, json_file, ensure_ascii=False, indent=4)

def import_modlist(mods):
    try:
        with open("modlist.json", "r", encoding="utf-8") as json_file:
            modlist = json.loads(json_file.read())
        return modlist
    except:
        return False
