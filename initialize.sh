#!/bin/bash

if [ ! -f env/bin/activate ]
then
	sudo apt install python-virtualenv
	virtualenv env --python=python3
fi
    .env/bin/activate
pip install -r requirements.txt