#!/bin/bash
gunicorn -w 4 -b 0.0.0.0 --daemon main:app && python3 scheduler.py