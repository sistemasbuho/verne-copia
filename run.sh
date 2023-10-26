#!/bin/bash  

# run local server
#ip="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"

if [ "$#" = "0" ] 
then
	python3 manage.py runserver 0.0.0.0:8010
else
	python3 manage.py runserver 0.0.0.0:$1
fi
