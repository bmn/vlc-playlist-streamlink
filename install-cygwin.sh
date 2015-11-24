#!/bin/bash

testing="Checking for Python:"
if hash python 2>/dev/null; then
	echo "$testing [OK]"
else
	echo "$testing [NA]"
	echo "Please install the packages 'python' and 'python-setuptools' using Cygwin's package manager"
	exit 1
fi

python $(dirname "$(readlink -f "$0")")/install.py cygwin
exit $?