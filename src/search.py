def find_mod(Mods, Keyword):
    items = []
    for Mod in Mods:
        items.append(Mod.name)

    #Search

    for position, item in enumerate(items):
        if item == Keyword:
            return Mods[position]

    return False
