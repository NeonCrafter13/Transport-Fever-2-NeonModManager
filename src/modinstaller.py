import os, configparser, subprocess
from distutils.dir_util import copy_tree

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])
sevenZipinstallation = os.path.normpath(config["DIRECTORY"]["7-zipInstallation"])

def install(link):
    if link.lower().endswith('zip') or link.lower().endswith('rar') or link.lower().endswith("7z"):
        subprocess.Popen(f'"{ os.path.join(sevenZipinstallation, "7z.exe") }" x {link} -o"{externalModsDirectory}" -y')
        return True
    if os.path.isdir(link):
        # copy subdirectory example
        _, b = os.path.split(link)
        copy_tree(link, os.path.join(externalModsDirectory, b))
        return True
