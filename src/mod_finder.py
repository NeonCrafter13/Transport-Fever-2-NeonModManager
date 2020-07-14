import os, re, json

from mod import Mod

def getExternalMod(folder):

    mod_lua = open(os.path.join(folder, "mod.lua"), "r", encoding="utf-8")
    mod_lua_text = mod_lua.read()
    authors = None
    name = None
    minorVersion = None
    try:
        mod_json = open(os.path.join(folder, "mod.json"), "r", encoding="utf-8")
    except:
        mod_json = None

    if mod_json:
        mod_json = json.loads(mod_json.read())
        name = mod_json["name"]
        authors = mod_json["authors"]
        minorVersion = mod_json["minorVersion"]

    if not name:
        x = re.search("name.*=.*_.*,", mod_lua_text)
        if x:
            y = re.search('".*"', x.group())
            if y != None:
                name = y.group()[1: len(y.group())-1]
            else:
                name = x.group()[10: len(x.group())-3]
        else:
            x = re.search("name.*=.*,", mod_lua_text)
            y = re.search('".*"', x.group())
            if y != None:
                name = y.group()[1: len(y.group())-1]
            else:
                name = x.group()[9: len(x.group())-3]

    if name == "mod_name":
        with open(os.path.join(folder, "strings.lua"), "r", encoding="utf-8") as strings_lua:
            strings_lua_text = strings_lua.read()
        x = re.search('mod_name.*=.*,', strings_lua_text)
        name = x.group()[14:len(x.group())-2]
    elif name == "name":
        with open(os.path.join(folder, "strings.lua"), "r", encoding="utf-8") as strings_lua:
            strings_lua_text = strings_lua.read()
        x = re.search('name.*=.*,', strings_lua_text)
        name = x.group()[10:len(x.group())-2]
    elif name == "title":
        with open(os.path.join(folder, "strings.lua"), "r", encoding="utf-8") as strings_lua:
            strings_lua_text = strings_lua.read()
        x = re.search('title.*=.*,', strings_lua_text)
        name = x.group()[9:len(x.group())-2]

    if not minorVersion:
        x = re.search("minorVersion.*=.*,", mod_lua_text)
        if x:
            x = x.group()[11: len(x.group())-1]
            minorVersion = int(re.findall("[0-9]", x)[0])
        else:
            minorVersion = None

    x = re.search("tfnetId.*,", mod_lua_text)
    if x:
        source = "transportfever.net"
    else:
        source = "other"

    try:
        image = open(os.path.join(folder,"workshop_preview.jpg"), "r")
        image = os.path.join(folder,"workshop_preview.jpg")
    except:
        image = None

    x = re.search("options.*=.*{", mod_lua_text)
    if x:
        options = True
    else:
        try:
            open(os.path.join(folder,"settings.lua"), "r")
            options = True
        except:
            options = False

    return Mod(name, minorVersion, source, image, options, folder, authors)
def getExternalMods(externalModsDirectory):
    folders = os.listdir(externalModsDirectory)

    try:
        folders.remove("readme.txt")
    except:
        pass
    Mods = []
    for folder in folders:
        try:
            Mods.append(getExternalMod(os.path.join(externalModsDirectory, folder)))
        except:
            continue
    return Mods

def getUserdataMods(userdataModsDirectory):
    folders = os.listdir(userdataModsDirectory)

    try:
        folders.remove("readme.txt")
    except:
        pass
    Mods = []
    for folder in folders:
        try:
            Mods.append(getExternalMod(os.path.join(userdataModsDirectory, folder)))
        except:
            continue
    return Mods

def getStagingAreaMods(StagingAreaModsDirectory):
    folders = os.listdir(StagingAreaModsDirectory)

    try:
        folders.remove("readme.txt")
    except:
        pass
    Mods = []
    for folder in folders:
        try:
            Mods.append(getExternalMod(os.path.join(StagingAreaModsDirectory, folder)))
        except:
            continue
    return Mods

def getSteamMod(folder):
    mod_lua = open(os.path.join(folder, "mod.lua"), "r", encoding="utf-8")
    mod_lua_text = mod_lua.read()
    authors = None
    name = None
    minorVersion = None
    try:
        mod_json = open(os.path.join(folder, "mod.json"), "r", encoding="utf-8")
    except:
        mod_json = None

    if mod_json:
        mod_json = json.loads(mod_json.read())
        name = mod_json["name"]
        authors = mod_json["authors"]
        minorVersion = mod_json["minorVersion"]

    if not name:
        x = re.search("name.*=.*_.*,", mod_lua_text)
        if x:
            y = re.search('".*"', x.group())
            if y != None:
                name = y.group()[1: len(y.group())-1]
            else:
                name = x.group()[10: len(x.group())-3]
        else:
            x = re.search("name.*=.*,", mod_lua_text)
            y = re.search('".*"', x.group())
            if y != None:
                name = y.group()[1: len(y.group())-1]
            else:
                name = x.group()[9: len(x.group())-3]

    if name == "mod_name":
        with open(os.path.join(folder, "strings.lua"), "r", encoding="utf-8") as strings_lua:
            strings_lua_text = strings_lua.read()
        x = re.search('mod_name.*=.*,', strings_lua_text)
        name = x.group()[14:len(x.group())-2]
    elif name == "name":
        with open(os.path.join(folder, "strings.lua"), "r", encoding="utf-8") as strings_lua:
            strings_lua_text = strings_lua.read()
        x = re.search('name.*=.*,', strings_lua_text)
        name = x.group()[10:len(x.group())-2]
    elif name == "title":
        with open(os.path.join(folder, "strings.lua"), "r", encoding="utf-8") as strings_lua:
            strings_lua_text = strings_lua.read()
        x = re.search('title.*=.*,', strings_lua_text)
        name = x.group()[9:len(x.group())-2]


    if not minorVersion:
        x = re.search("minorVersion.*=.*,", mod_lua_text)
        if x:
            x = x.group()[11: len(x.group())-1]
            minorVersion = int(re.findall("[0-9]", x)[0])
        else:
            minorVersion = None

    source = "Steam"

    try:
        image = open(os.path.join(folder,"workshop_preview.jpg"), "r")
        image = os.path.join(folder,"workshop_preview.jpg")
    except:
        image = None

    x = re.search("options.*=.*{", mod_lua_text)
    if x:
        options = True
    else:
        try:
            open(os.path.join(folder,"settings.lua"), "r")
            options = True
        except:
            options = False

    return Mod(name, minorVersion, source, image, options, folder, authors)

def getSteamMods(steamModsDirectory):
    folders = os.listdir(steamModsDirectory)

    try:
        folders.remove("readme.txt")
    except:
        pass
    Mods = []
    for folder in folders:
        try:
            Mods.append(getExternalMod(os.path.join(steamModsDirectory, folder)))
        except:
            continue
    return Mods

def getAllMods(externalModsDirectory, steamModsDirectory, userdataModsDirectory, StagingAreaModsDirectory):
    Mods = []
    for mod in getExternalMods(externalModsDirectory):
        Mods.append(mod)
    for mod in getSteamMods(steamModsDirectory):
        Mods.append(mod)
    for mod in getUserdataMods(userdataModsDirectory):
        Mods.append(mod)
    for mod in getStagingAreaMods(StagingAreaModsDirectory):
        Mods.append(mod)
    return Mods
