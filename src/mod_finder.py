import os, re

from Mod import Mod

from helpfunctions import *

def getMod(folder):

    mod_lua = open(os.path.join(folder, "mod.lua"), "r")
    print(folder)
    mod_lua_text = mod_lua.read()
    x = re.search("name = _.*,", mod_lua_text)
    name = x.group()[10: len(x.group())-3]
    print(name)
def getExternalMods(externalModsDirectory):
    folders = os.listdir(externalModsDirectory)

    folders.remove("readme.txt")
    for folder in folders:
        getMod(os.path.join(externalModsDirectory, folder))



getExternalMods("C:\Program Files (x86)\Steam\steamapps\common\Transport Fever 2\mods")
