#!/bin/bash

DIR=$(dirname "$(readlink -f "$0")")

# Python
testing="Checking for Python:"
if hash python 2>/dev/null; then
	echo "$testing [OK]"
else
	echo "$testing [NA]"
	echo "Please install the packages 'python' and 'python-setuptools' using Cygwin's package manager"
	exit 1
fi

# PIP or easy_install
testing="Checking for PIP package manager:"
if hash pip 2>/dev/null; then
	echo "$testing [OK]"
	py_pacman="pip install"
else
	echo "$testing [NA]"
	testing="Checking for easy_install package manager:"
	if hash easy_install 2>/dev/null; then
		echo "$testing [OK]"
		py_pacman="easy_install"
	else
		echo "$testing [NA]"
		echo "Please install the package 'python-setuptools' using Cygwin's package manager"
		exit 1
	fi
fi

# Livestreamer and six
testing="Checking for Python modules (Livestreamer, six):"
command="import livestreamer, six"
if python -c "$command" >/dev/null 2>&1; then
	echo "$testing [OK]"
else
	echo "$testing [NA]"
	echo "Attempting to install modules:"
	if $py_pacman livestreamer six; then
		testing="Rechecking for Python modules:"
		if python -c "$command"; then
			echo "$testing [OK]"
		else
			echo "$testing [NA]"
			echo "Module install appears to have failed. Please try installing the modules 'livestreamer' and 'six' manually."
			exit 1
		fi
	else
		echo "Module install appears to have failed. Please try installing the modules 'livestreamer' and 'six' manually."
		exit 1
	fi
fi

# Install service
if cygrunsrv -Q 'Livestreamer Service' >/dev/null 2>&1; then
	echo "Windows livestreamersrv service already exists, skipping installation."
else
	testing="Checking livestreamersrv service:"
	echo "Installing livestreamersrv as a Windows service (requires Administrator privileges)"
	read -p "Press ENTER to continue"
	cygstart --action=runas cmd.exe /k "$(cygpath -wa $(which cygrunsrv)) -I 'Livestreamer Service' -p $DIR/livestreamersrv/livestreamersrv & exit"
	sleep 1 # gives Windows a chance to catch up
	if cygrunsrv -Q 'Livestreamer Service' >/dev/null 2>&1; then
		echo "$testing [OK]"
		echo "Starting livestreamersrv (requires Administrator privileges)"
		read -p "Press ENTER to continue"
		cygstart --action=runas cmd.exe /k "$(cygpath -wa $(which cygrunsrv)) -S 'Livestreamer Service' & exit"
	else
		echo "$testing [NA]"
		echo "Service install appears to have failed. To start the service manually, use the command:"
		echo "./livestreamersrv/livestreamersrv start"
	fi
fi

# Find VLC install directory
testing="Looking for VLC Lua directory:"
lua_path="\VideoLAN\VLC\lua\playlist" # Using Windows-style paths because some Cygwin distros (e.g. MobaXterm) don't use /cygdrive
vlc_path="C:\Program Files"
if [ -d "$vlc_path$lua_path" ]; then
	lua_path="$vlc_path$lua_path"
	echo "$testing $lua_path"
else
	vlc_path="C:\Program Files (x86)"
	if [ -d "$vlc_path$lua_path" ]; then
		lua_path="$vlc_path$lua_path"
		echo "$testing $lua_path"
	else
		echo "$testing [NA]"
		echo "VLC directory not found. Please copy vlc/livestreamer.lua to the directory lua/playlist in your VLC installation."
		exit 1
	fi
fi

# Install vlc-playlist-livestreamer
testing="Checking vlc-playlist-livestreamer VLC plugin:"
lua_path="$lua_path\livestreamer.lua"
echo "Installing vlc-playlist-livestreamer VLC plugin (requires Administrator privileges)"
read -p "Press ENTER to continue"
cygstart --action=runas cmd.exe /k "echo Installing vlc-playlist-livestreamer VLC plugin: & copy \"$(cygpath -wa $(pwd)/vlc/livestreamer.lua)\" \"$lua_path\" & exit"
sleep 1
if [ -f "$lua_path" ]; then
	echo "$testing [OK]"
else
	echo "$testing [NA]"
	echo "Plugin install appears to have failed. Please copy vlc/livestreamer.lua to the directory lua/playlist in your VLC installation."
	exit 1
fi
	
# Done!
echo "Installation complete!"
exit 0