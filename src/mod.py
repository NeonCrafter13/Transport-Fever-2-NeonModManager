import shutil

class Mod():
    def __init__(self, name, minorVersion, source, image, options, location, authors, category_image):
        self.name = name
        self.minorVersion = minorVersion
        self.source = source
        self.image = image
        self.options = options
        self.location = location
        self.authors = authors
        self.category_image = category_image

    def uninstall(self):
        try:
            shutil.rmtree(self.location)
            return True
        except:
            return False
