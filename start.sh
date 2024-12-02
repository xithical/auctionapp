#!/bin/bash
pip3 install -r requirements.txt
python3 init.py
gunicorn -w 4 -b 0.0.0.0 --daemon --capture-output --enable-stdio-inheritance main:app && python3 scheduler.py
