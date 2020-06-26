# Entrypoint to the Aplication
import configparser
import os


config = configparser.ConfigParser()
config.read("settings.ini")
print(config.sections())
print(config['DIRECTORY']['externalMods'])
