#!/bin/bash
python -m pip install -r requirements/prod.txt
python manage.py collectstatic --noinput
