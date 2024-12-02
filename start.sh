#!/bin/bash
python3 init.py
gunicorn -w 4 -b 0.0.0.0 --daemon --capture-output --enable-stdio-inheritance main:app && python3 scheduler.py