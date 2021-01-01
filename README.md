# Transport-Fever-2-NeonModManager
A Mod-Manager for Transport Fever 2 written in Python.

:de:
### Funktionen:

Auflisten aller installierten Mods,
Suche der installierten Mods,
Öffnen der Mod,
Deinstallieren der Mod,
Exportiere Modlisten,
vergleiche Modlisten mit installierten Mods.


In der neuen Version benötigt ihr 7-Zip um dieses Programm zu verwenden.



### Information für Modder:

Falls eure Mod nicht richtig erkannt wird könnt ihr dass beheben in dem ihr eine Mod.json anlegt wie in diesem Beispiel:

https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/blob/v1.3/example/mod.json und diesen in eure Mod packt.

:uk:
### What you can do with this Apllication:

List all installed Mods,
Search your installed Mods,
Open a Mod in Explorer,
Uninstall a Mod,
export modlists,
compare modlists with installed mods.
To run this apllication you need 7-Zip.



### Information for Modders:

If your Mod is not detected correct create a File called Mod.json in your Mod as in the Example:https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/blob/v1.3/example/mod.json

## Installation

:de:
### Windows
Um für Windows den NeonModManager zu installieren lädst du dir auf Github die Windows Version runter(https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/releases/latest).
Ihr müsst außerdem 7-zip installieren um dieses Programm zu verwenden.
In der settings.ini Datei(umbennent die example_settings.ini) befinden sich die Pfade zu den Mods, bei "externalmods" sollte der Dateipfad zum Mod-Verzeichnis stehen, wo die Mods von z.B transportfever.net installiert sind.
Bei "steammods" sollte ein Link zu den Steam-Mod-Verzeichnis liegen.
Bei userdatamods sollte der Pfad zu dem UserdataMods stehen.
Bei stagingaremods sollte der Pfad zur stagingArea eingetragen sein.
Bei 7-zipInstallation müsst ihr den Pfad zu eurer 7.Zip installation eintragen.
Wenn ihr fertig seit führt die Main.exe aus.
Erklärung in Videoform: https://youtu.be/MfPp4Gdmft4
### Linux Debian based Systems
Gehe auf den letzten Release und downloade dir die .deb Datei. Doppelklicke die Datei und klicke auf Installieren.
Navigiere dann zu dem Pfad `/usr/share/Tpf2NeonModManager` erstelle dort die Datei settings.ini.
In der settings.ini stellst du alles richtig ein. Der 7-Zip Pfad muss nur ein existierender Pfad sein es funktionier auch jeder andere Pfad.
Beispiel settings.ini:
```
[DIRECTORY]
externalmods = /home/marek/.steam/debian-installation/steamapps/common/Transport Fever 2/mods
steammods = /home/marek/.steam/debian-installation/steamapps/workshop/content/1066780 
userdatamods = /home/marek/.steam/debian-installation/userdata/436684792/1066780/local/mods
stagingareamods = /home/marek/.steam/debian-installation/userdata/436684792/1066780/local/staging_area
7-zipInstallation = /usr

[GRAPHICS]
modernstyle = True
imagesize = 384
```
Anschließend solltest du in deinem Menu den NeonModManager finden können.

:uk:
### Windows
For installation under Windows download the Windows realease via Github.https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager/releases/latest).
You also need to install 7-zip.
In the settings.ini File(rename example_settings.ini) are Paths to the Mods´ folders , at "externalmods" should be the Path to the Mod-Directory, where the Mods are from for Example transportfever.net.
At "steammods" should be a Path to the Steam-Mod-Directory.
At userdatamods should be the Path to the UserdataMods.
At stagingaremods should be the Path to the stagingArea.
At 7-zipInstallation you should put the Path to your 7-Zip installation.
If your ready start the Main.exe file.
### Linux Debian based Systems
Go to the last release and download the .deb file. Click on the file and hit install. You will be requiered to type in you're Password.
Navigate to the Pathe `/usr/share/Tpf2NeonModManager`, there you create a file called Settings.ini.
In this Settings.ini file you enter your files an example can be found below. The 7zip Path doesn't need to be correct, it just needs to be a existing path.
Example settings.ini:
```
[DIRECTORY]
externalmods = /home/marek/.steam/debian-installation/steamapps/common/Transport Fever 2/mods
steammods = /home/marek/.steam/debian-installation/steamapps/workshop/content/1066780 
userdatamods = /home/marek/.steam/debian-installation/userdata/436684792/1066780/local/mods
stagingareamods = /home/marek/.steam/debian-installation/userdata/436684792/1066780/local/staging_area
7-zipInstallation = /usr

[GRAPHICS]
modernstyle = True
imagesize = 384
```
After those steps you should be able to find Tpf2-NeonModManager in you Menu.

Also Available via Transport-Fever.net https://www.transportfever.net/filebase/index.php?entry/5573-neonmodmanager-ein-mod-manager-f%C3%BCr-transport-fever-2/
