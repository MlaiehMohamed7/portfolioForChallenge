#!/bin/bash


echo "access to root privilege required"
sudo echo "please enter your password to get the access"

if [ -e "/usr/lib/python3/" ];then
	sudo cp "./osint.py" "/usr/lib/python3/osint.py"
elif [ ${#1} -gt 0 ];then
	sudo cp "./osint.py" ${1}
else
	echo "please add the python3 library directory as a first parameter"
	exit
fi

if [ -e "/bin/pip3" ];then
	echo "you already have pip3"
	echo "we will make sure it is updated"
	sudo apt update pip3
	echo "installing extra required library"
	pip3 install phonenumbers
	pip3 install PIL
	echo "everything is setted and ready to ignite"
else
	echo "automatic setting initialized"
	sudo apt install pip3
	echo "pip3 installed"
	echo "installing extra required library"
	pip3 install phonenumbers
	pip3 install PIL
	echo "everything is setted and ready to ignite"
fi

sudo apt install theharvester
sudo apt install whois
