import shutil

class Mod():
    def __init__(self, name, minorVersion, source, image, options, location, authors):
        self.name = name
        self.minorVersion = minorVersion
        self.source = source
        self.image = image
        self.options = options
        self.location = location
        self.authors = authors

    def uninstall(self):
        try:
            shutil.rmtree(self.location)
            return True
        except:
            return False
