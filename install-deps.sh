#!/bin/bash

#load virtual env
if [ ! $VIRTUAL_ENV ]; then
	echo "... loading virtual environment"
	. venv/bin/activate
fi

pip install $(cat requirements.txt | tr '\n' ' ')

