#!/bin/bash  

if [ "$*" = "requirements-docker" ] 
then
	# Install required packages
	apt-get -qq install -y -u python3 xorg xvfb dbus-x11 xfonts-100dpi xfonts-75dpi xfonts-cyrillic curl ghostscript firefox xvf dpkg openssh-server wget libpq-dev python3-dev python3-setuptools git-core python3-pip build-essential nano python3-psycopg2

	#upgrade pip
	pip3 install --upgrade pip

fi

if [ "$*" = "requirements" ] 
then
	# Install required packages
	apt-get -qq install -y -u python3 xorg xvfb dbus-x11 xfonts-100dpi xfonts-75dpi xfonts-cyrillic curl ghostscript imagemagick convmv firefox xvfb dpkg openssh-server wget libpq-dev python-dev python-setuptools git-core python3-pip build-essential mysql-client nano wkhtmltopdf phantomjs python-psycopg2

	#upgrade pip
	sudo pip3 install --upgrade pip

	#install requirements
	sudo pip3 install -r requirements.txt

fi

if [ "$*" = "new_db" ] 
then
	python3 manage.py migrate ingestiondemo zero 
	python3 manage.py makemigration 
	python3 manage.py migrate 
fi

if [ "$*" = "update_db" ] 
then
	python3 manage.py makemigration 
	python3 manage.py migrate 
fi

if [ "$*" = "static" ] 
then
	python3 manage.py collectstatic
fi

if [ "$*" = "reset_pass" ] 
then
	python3 manage.py changepassword admin
fi

# if [ "$*" = "postgres-dump" ] 
# then
# 	'pg_dump -h localhost -p 5432 -U ingestion_admin -F c -b -v -f "/webapp/fenosa/backups/fenosa$(date +%Y-%m-%d-%H_%M).backup" fenosa_2018'
# fi

# if [ "$*" = "postgres-restore" ] 
# then
# 	'pg_restore -h localhost -p 5432 -U ingestion_admin -d fenosa_2018 -v "/webapp/fenosa/fenosa-producion.backup"'
# fi
