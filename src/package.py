import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
resources = [
    ('./images', './images'),
    ('./modlist.json', './modlist.json'),
    ('./settings.ini', './settings.ini'),
    ('./aqua.css', './aqua.css'),
]
build_exe_options = {
    'include_files': resources
}

build_mac_options = {
    'iconfile': './images/Icon.icns',
    'bundle_name': 'Transport Fever 2 NeonModManager',  # Name of the application: <name>.app
    'codesign_identity': "willwill2will@gmail.com",
    'codesign_deep': True
}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Tpf2 NeonModManager",
    version="1.11a1",
    description="A little ModManager written in Python. See more info at https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager.",
    options={'build_exe': build_exe_options, 'bdist_mac': build_mac_options},
    executables=[Executable("main.py", base=base, target_name='NeonModManager')]
)
