#!/bin/bash

echo 'Setuping the python environment and dependencies...'
python3 -m venv env && \
source env/bin/activate && \
pip3 install -r training/requirements.txt
pip3 install -r feature-extract/requirements.txt
deactivate
echo 'Setuping the python environment and dependencies done!'