#!/bin/bash
pip install -r requirements.txt
gunicorn web_app:app --host 0.0.0.0 --port $PORT
