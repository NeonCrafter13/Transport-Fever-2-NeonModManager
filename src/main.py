# Entrypoint to the Aplication
import configparser
import os
import ast

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])

folders = os.listdir(externalModsDirectory)
folders.remove("readme.txt")
print(folders)
for folder in folders:
    mod_lua = open(os.path.join(externalModsDirectory,folder, "mod.lua"), "r")
    print(eval(mod_lua.read()))
