#!/bin/bash

#load virtual env
if [ ! $VIRTUAL_ENV ]; then
	echo "... loading virtual environment"
	. venv/bin/activate
fi
echo "" > ./install-deps.log
pip install $(cat requirements.txt | tr '\n' ' ') --log ./install-deps.log

