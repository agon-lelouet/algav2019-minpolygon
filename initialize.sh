#!/bin/sh

if [ ! "$(command -v virtualenv)" ]; then
    sudo apt install python-virtualenv
fi

if [ ! -f "env/bin/activate" ]; then
    virtualenv env --python=python3
fi

. env/bin/activate
pip install -r requirements.txt
