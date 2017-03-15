#!/bin/bash
pip install $(cat requirements.txt | tr '\n' ' ')
