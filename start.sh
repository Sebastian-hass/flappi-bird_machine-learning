#!/bin/bash
pip install -r requirements.txt
gunicorn web_app:app --bind 0.0.0.0:$PORT
