#!/bin/bash
echo "Python version:"
python --version
echo "Pip version:"
python -m pip --version
python -m pip install -r requirements/prod.txt
python manage.py collectstatic --noinput
