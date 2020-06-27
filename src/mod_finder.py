import os

from Mod import Mod

from helpfunctions import *

from luaparser import ast
from luaparser import astnodes

def getMod(folder):

    mod_lua = open(os.path.join(folder, "mod.lua"), "r")
    print(folder)
    mod_lua_text = mod_lua.read()
    """
    tree = ast.parse(mod_lua.read())

    for node in ast.walk(tree):
        if isinstance(node, astnodes.Name):
            print(node)
    """
    """
    class NumberVisitor(ast.ASTVisitor):
        def visit_Number(self, node):
            print('Number value = ' + str(node))
    """
    a = find_str(mod_lua_text, "minorVersion")
    minorVersion = mod_lua_text[a + 15]
    # print(a)



    tree = ast.parse(mod_lua_text)

    for node in ast.walk(tree):
        if isinstance(node, astnodes.Name):
            print(node)
def getExternalMods(externalModsDirectory):
    folders = os.listdir(externalModsDirectory)

    folders.remove("readme.txt")
    for folder in folders:
        getMod(os.path.join(externalModsDirectory, folder))



getExternalMods("C:\Program Files (x86)\Steam\steamapps\common\Transport Fever 2\mods")
