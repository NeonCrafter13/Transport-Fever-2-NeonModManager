import json

def export_modlist(mods):
    mods_json = []
    for mod in mods:
        mod_json = {"name": mod.name, "source": mod.source, "authors": mod.authors}
        mods_json.append(mod_json)
    json_file = open("modlist.json", "w")
    json_file.write(json.dumps(mods_json))

def import_modlist(mods):
    pass
