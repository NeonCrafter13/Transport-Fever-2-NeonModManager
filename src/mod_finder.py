import concurrent.futures
import os
import re
import json
import operator

from mod import Mod

def execute_without_error(func, arg):
    try:
        return func(arg)
    except:
        return None

def getName(folder, mod_lua_text):
    x = re.search("name.*=.*_.*,", mod_lua_text)
    if x:
        y = re.search('".*"', x.group())
        if y is not None:
            name = y.group()[1: len(y.group()) - 1]
        else:
            name = x.group()[10: len(x.group()) - 3]
    else:
        x = re.search("name.*=.*,", mod_lua_text)
        y = re.search('".*"', x.group())
        if y is not None:
            name = y.group()[1: len(y.group()) - 1]
        else:
            name = x.group()[9: len(x.group()) - 3]

    try:
        with open(os.path.join(folder, "strings.lua"), "r", encoding="utf-8") as strings_lua:
            strings_lua_text = strings_lua.read()
        x = re.search(f'{name}.*', strings_lua_text)
        y = re.search('".*"', x.group()[len(name) + 1:])
        name = y.group()[1:len(y.group()) - 1]
    except FileNotFoundError:
        pass

    return name

def get_Category(folder):
    try:
        s = os.listdir(os.path.join(folder, "res", "textures", "ui", "construction", "categories"))
    except:
        return None
    if s == []:
        return None
    else:
        return os.path.join(folder, "res", "textures", "ui", "construction", "categories", s[0])

def getExternalMod(folder):

    mod_lua = open(os.path.join(folder, "mod.lua"), "r", encoding="utf-8")
    mod_lua_text = mod_lua.read()
    authors = None
    name = None
    minorVersion = None
    try:
        mod_json = open(os.path.join(folder, "mod.json"), "r", encoding="utf-8")
    except FileNotFoundError:
        mod_json = None

    if mod_json:
        mod_json = json.loads(mod_json.read())
        name = mod_json["name"]
        authors = mod_json["authors"]
        minorVersion = mod_json["minorVersion"]

    if not name:
        name = getName(folder, mod_lua_text)

    if not minorVersion:
        x = re.search("minorVersion.*=.*,", mod_lua_text)
        if x:
            x = x.group()[11: len(x.group()) - 1]
            minorVersion = int(re.findall("[0-9]", x)[0])
        else:
            minorVersion = None

    x = re.search("tfnetId.*,", mod_lua_text)
    if x:
        source = "transportfever.net"
    else:
        source = "other"

    try:
        image = open(os.path.join(folder, "workshop_preview.jpg"), "r")
        image = os.path.join(folder, "workshop_preview.jpg")
    except FileNotFoundError:
        image = None

    x = re.search("options.*=.*{", mod_lua_text)
    if x:
        options = True
    else:
        try:
            open(os.path.join(folder, "settings.lua"), "r")
            options = True
        except FileNotFoundError:
            options = False

    category_image = get_Category(folder)

    return Mod(name, minorVersion, source, image, options, folder, authors, category_image)

def getExternalMods(externalModsDirectory):
    folders = os.listdir(externalModsDirectory)

    try:
        folders.remove("readme.txt")
    except:
        pass
    Mods = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        threads = []
        for folder in folders:
            threads.append(executor.submit(execute_without_error,
                                           getExternalMod,
                                           os.path.join(externalModsDirectory, folder)))

        for thread in threads:
            result = thread.result()
            if result:
                Mods.append(result)
    return Mods


def getUserdataMods(userdataModsDirectory):
    folders = os.listdir(userdataModsDirectory)

    try:
        folders.remove("readme.txt")
    except:
        pass
    Mods = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        threads = []
        for folder in folders:
            threads.append(executor.submit(execute_without_error,
                                           getExternalMod,
                                           os.path.join(userdataModsDirectory, folder)))

        for thread in threads:
            result = thread.result()
            if result:
                Mods.append(result)
    return Mods

def getStagingAreaMods(StagingAreaModsDirectory):
    folders = os.listdir(StagingAreaModsDirectory)

    try:
        folders.remove("readme.txt")
    except:
        pass
    Mods = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        threads = []
        for folder in folders:
            threads.append(executor.submit(execute_without_error,
                                           getExternalMod,
                                           os.path.join(StagingAreaModsDirectory, folder)))

        for thread in threads:
            result = thread.result()
            if result:
                Mods.append(result)
    return Mods

def getSteamMod(folder):
    mod_lua = open(os.path.join(folder, "mod.lua"), "r", encoding="utf-8")
    mod_lua_text = mod_lua.read()
    authors = None
    name = None
    minorVersion = None
    try:
        mod_json = open(os.path.join(folder, "mod.json"), "r", encoding="utf-8")
    except FileNotFoundError:
        mod_json = None

    if mod_json:
        mod_json = json.loads(mod_json.read())
        name = mod_json["name"]
        authors = mod_json["authors"]
        minorVersion = mod_json["minorVersion"]

    if not name:
        name = getName(folder, mod_lua_text)

    if not minorVersion:
        x = re.search("minorVersion.*=.*,", mod_lua_text)
        if x:
            x = x.group()[11: len(x.group()) - 1]
            minorVersion = int(re.findall("[0-9]", x)[0])
        else:
            minorVersion = None

    source = "Steam"

    try:
        image = open(os.path.join(folder, "workshop_preview.jpg"), "r")
        image = os.path.join(folder, "workshop_preview.jpg")
    except FileNotFoundError:
        image = None

    x = re.search("options.*=.*{", mod_lua_text)
    if x:
        options = True
    else:
        try:
            open(os.path.join(folder, "settings.lua"), "r")
            options = True
        except FileNotFoundError:
            options = False

    category_image = get_Category(folder)

    return Mod(name, minorVersion, source, image, options, folder, authors, category_image)

def getSteamMods(steamModsDirectory):
    folders = os.listdir(steamModsDirectory)

    try:
        folders.remove("readme.txt")
    except:
        pass
    Mods = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        threads = []
        for folder in folders:
            threads.append(executor.submit(execute_without_error,
                                           getSteamMod, os.path.join(steamModsDirectory, folder)))

        for thread in threads:
            result = thread.result()
            if result:
                Mods.append(result)
    return Mods

def getAllMods(externalModsDirectory, steamModsDirectory, userdataModsDirectory, StagingAreaModsDirectory):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        t1 = executor.submit(getExternalMods, externalModsDirectory)
        t2 = executor.submit(getSteamMods, steamModsDirectory)
        t3 = executor.submit(getUserdataMods, userdataModsDirectory)
        t4 = executor.submit(getStagingAreaMods, StagingAreaModsDirectory)
        externalmods = t1.result()
        steammods = t2.result()
        userdatamods = t3.result()
        stagingareamods = t4.result()
    Mods = []
    for mod in externalmods:
        Mods.append(mod)
    for mod in steammods:
        Mods.append(mod)
    for mod in userdatamods:
        Mods.append(mod)
    for mod in stagingareamods:
        Mods.append(mod)
    Mods = sorted(Mods, key=operator.attrgetter('name'))
    return Mods
