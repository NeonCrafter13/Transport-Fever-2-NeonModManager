import os, zipfile, configparser, rarfile
from distutils.dir_util import copy_tree

config = configparser.ConfigParser()
config.read("settings.ini")

externalModsDirectory = os.path.normpath(config['DIRECTORY']['externalMods'])

def install(link):
    print(link)
    if link.lower().endswith(('zip')):
        ZipFile = zipfile.ZipFile(link, mode="r")
        ZipFile.extractall(path=externalModsDirectory)
        return True
    if link.lower().endswith(('rar')):
        RarFile = rarfile.RarFile(link, mode="r")
        RarFile.extractall(path=externalModsDirectory)
        return True
    if os.path.isdir(link):
        # copy subdirectory example
        _, b = os.path.split(link)
        copy_tree(link, os.path.join(externalModsDirectory, b))
        return True
