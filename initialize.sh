#!/bin/sh

if [ ! "$(command -v virtualenv)" ]; then
    sudo apt install python-virtualenv
    sudo apt install python3-tk
fi

if [ ! -f "env/bin/activate" ]; then
    virtualenv env --python=python3
fi

source env/bin/activate
pip install -r requirements.txt
