# Entrypoint to the Aplication
import configparser



config = configparser.ConfigParser()
config.read('../settings.ini')
print(config.sections())
print(config['DIRECTORY']['externalMods'])
