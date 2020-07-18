import mod_finder
import os
import time

def Average(data: list):
    o = len(data)
    a = 0
    for i in data:
        a = a + i
    return a / o

runtimes = []

for i in range(20):
    a = time.time()
    args = (
    os.path.normpath("C:/Program Files (x86)/Steam/steamapps/common/Transport Fever 2/mods"),
    os.path.normpath("C:/Program Files (x86)/Steam/steamapps/workshop/content/1066780"),
    os.path.normpath("C:/Program Files (x86)/Steam/userdata/436684792/1066780/local/mods"),
    os.path.normpath("C:/Program Files (x86)/Steam/userdata/436684792/1066780/local/staging_area")
    )
    mod_finder.getAllMods(*args)
    b = time.time()
    runtime = b - a
    runtimes.append(runtime)

print(Average(runtimes))
