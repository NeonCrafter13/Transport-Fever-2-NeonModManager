# Entrypoint to the Aplication
import configparser
import os


config = configparser.ConfigParser()
config.read(os.path.abspath("../settings.ini"))
print(config.sections())
print(config['DIRECTORY']['externalMods'])
