import sys, os, zipfile, configparser, rarfile

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
        print("FOLDER")
