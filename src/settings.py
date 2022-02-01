import configparser
import os
from freezeutils import find_data_file as f

class Settings():
    def load(self):
        config = configparser.ConfigParser()

        a = config.read(os.path.abspath(f("settings.ini")))

        try:
            self.image_width = int(config["GRAPHICS"]["imagesize"])
        except KeyError:
            self.image_width = 384

        try:
            self.style = config["GRAPHICS"]["modernstyle"]
            if self.style.lower().replace(" ", "") == "true":
                with open(f("Aqua.css"), "r") as style:
                    self.style = style.read()
            else:
                self.style = ""
        except KeyError:
            self.style = ""

        try:
            self.extern_mods_dir = os.path.normpath(
                config['DIRECTORY']['externalMods'])
            self.steam_mods_dir = os.path.normpath(config["DIRECTORY"]["steamMods"])
            self.userdata_mods_dir = os.path.normpath(
                config["DIRECTORY"]["userdatamods"])
            self.stagingarea_mods_dir = os.path.normpath(
                config["DIRECTORY"]["stagingareamods"])
            self.sevenzip_dir = os.path.normpath(
                config["DIRECTORY"]["7-zipInstallation"])

            self.language = config["LANGUAGE"]["language"]
        except:
            return False
        
        return True
