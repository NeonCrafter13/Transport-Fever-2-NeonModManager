import configparser, os

config = configparser.ConfigParser()
config.read("settings.ini")

try:
    print("externalmods found: " + os.path.normpath(config['DIRECTORY']['externalMods']))
except:
    print("externalmods not found!!!")

try:
    print("steammods found: " + os.path.normpath(config["DIRECTORY"]["steamMods"]))
except:
    print("steammods not found!!!")

try:
    print("userdatamods found: " + os.path.normpath(config["DIRECTORY"]["userdatamods"]))
except:
    print("userdatamods not found!!!")

try:
    print("stagingareamods found: " + os.path.normpath(config["DIRECTORY"]["stagingareamods"]))
except:
    print("stagingareamods not found!!!")

try:
    print("7-zip found: " + os.path.normpath(config["DIRECTORY"]["7-zipInstallation"]))
except:
    print("7-zip not found!!!")

input()
