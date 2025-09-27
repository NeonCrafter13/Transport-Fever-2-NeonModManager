import yaml

class Language():
    def __init__(self, selected_language: str) -> None:
        self.selected_language = selected_language
        self.data = None

    def load_lang(self):
        with open(f"translations/{self.selected_language}.yaml", "r") as f:
            a = yaml.load(f.read(), Loader=yaml.Loader)
        self.data = a

    def getTranslation(self, section: str, item: "str"):
        if self.data is None:
            raise Exception("Language not loaded")
            return
        return self.data[section][item]
