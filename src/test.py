import mod_finder

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
    "C:/Program Files (x86)/Steam/steamapps/common/Transport Fever 2/mods",
    "C:/Program Files (x86)/Steam/steamapps/workshop/content/1066780",
    "C:/Program Files (x86)/Steam/userdata/436684792/1066780/local/mods",
    "C:/Program Files (x86)/Steam/userdata/436684792/1066780/local/staging_area"
    )
    mod_finder.getAllMods(*args)
    b = time.time()
    runtime = b - a
    runtimes.append(runtime)

print(Average(runtimes))
