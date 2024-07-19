#!/bin/bash
python3.10 -m pip install -r requirements/prod.txt
python3.10 manage.py collectstatic --noinput
