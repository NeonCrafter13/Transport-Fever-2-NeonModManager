# Entrypoint to the Aplication
import configparser
import os
import mod_finder

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
steamModsDirectory = os.path.normpath(config["DIRECTORY"]["steamMods"])

print(mod_finder.getAllMods(externalModsDirectory, steamModsDirectory)[0])
