def find_mod(Mods, Keyword):
    Keyword = Keyword.lower().replace(" ","")
    items = []
    for Mod in Mods:
        name = Mod.name
        name = name.lower().replace(" ","")
        items.append(name)

    #Search

    for position, item in enumerate(items):
        if item == Keyword:
            return (Mods[position],position)

    return False
