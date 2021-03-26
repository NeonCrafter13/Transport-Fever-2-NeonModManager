Summary: A Mod Manager for Transport-Fever 2
Name: Tpf2-NeonModManager
Version: 1.11
Release: 1
License: GPLv3
URL: https://github.com/NeonCrafter13/Transport-Fever-2-NeonModManager
Group: Amusements/Games
Packager: NeonCrafter13
Requires: python3
Requires: PyQt5
Requires: python3-numpy
Requires: p7zip-plugins
BuildRoot: ~/rpmbuild/

%description
A simple Mod Manager written in Python, with which you can manage your mods in Transport-Fever-2.

%prep
echo "BUILDROOT = $RPM_BUILD_ROOT"
mkdir -p $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager
mkdir -p $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/images
mkdir -p $RPM_BUILD_ROOT/usr/share/applications

cp /home/mm/Transport-Fever-2-NeonModManager/src/main.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/main
cp /home/mm/Transport-Fever-2-NeonModManager/src/mod_finder.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/mod_finder.py
cp /home/mm/Transport-Fever-2-NeonModManager/src/modinstaller.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/modinstaller.py
cp /home/mm/Transport-Fever-2-NeonModManager/src/modlist.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/modlist.py
cp /home/mm/Transport-Fever-2-NeonModManager/src/search.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/search.py
cp /home/mm/Transport-Fever-2-NeonModManager/src/images.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/images.py
cp /home/mm/Transport-Fever-2-NeonModManager/src/mod.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/mod.py
cp /home/mm/Transport-Fever-2-NeonModManager/src/Aqua.css $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/Aqua.css
cp /home/mm/Transport-Fever-2-NeonModManager/src/modlist.json $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/modlist.json
cp /home/mm/Transport-Fever-2-NeonModManager/src/setup.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/setup.py
cp /home/mm/Transport-Fever-2-NeonModManager/src/images/* $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/images
cp /home/mm/Transport-Fever-2-NeonModManager/src/Tpf2-NeonModManager.desktop $RPM_BUILD_ROOT/usr/share/applications/Tpf2-NeonModManager.desktop
cp /home/mm/Transport-Fever-2-NeonModManager/src/freezeutils.py $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager/freezeutils.py

exit 

%files
%attr(-, root, root) /usr/share/applications/*
%attr(-, whoami, -) /usr/share/Tpf2NeonModManager/*

%clean
rm -rf $RPM_BUILD_ROOT/usr/share/Tpf2NeonModManager
rm -rf $RPM_BUILD_ROOT/usr/share/applications

%post
chmod 777 /usr/share/Tpf2NeonModManager

#rpmbuild --target noarch -bb Tpf2-NeonModManager.spec 
