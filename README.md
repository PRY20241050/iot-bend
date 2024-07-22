# IoT Monitoring Bend

## Description
This project is an API for air quality monitoring through sensors connected in an IoT network.
The project is developed using Django and Django REST Framework.

## Table of Contents
- [Description](#description)
- [Requirements](#requirements)
- [Quick start](#quick-start)
  - [Linux](#linux)
  - [Windows](#windows)
- [Initialize Server](#initialize-the-server)
- [Authors](#authors)

## Requirements
- Python 3.10

## Quick start
If you need to run the project locally, you can follow the steps below.
- Linux:
  ```bash
  # Create a virtual environment
  python3 -m venv venv
  # Activate the virtual environment
  source venv/bin/activate
  # Install the project dependencies
  pip install -r requirements/dev.txt
  # Copy the .env file
  cp environments/.env.template environments/.env
  # Apply the migrations
  python manage.py makemigrations
  python manage.py migrate
  # Initialize the server
  python manage.py runserver
  ```
- Windows:
  ```bash
  # Create a virtual environment
  py -m venv venv
  # Activate the virtual environment
  venv/Scripts/activate
  # Install the project dependencies
  pip install -r requirements/dev.txt
  # Copy the .env file
  copy environments/.env.template environments/.env
  # Apply the migrations
  py manage.py makemigrations
  py manage.py migrate
  # Initialize the server
  py manage.py runserver
  ```

### Initialize the server
To initialize the server you need to execute the following command.
  1. Activate the virtual environment ```venv/Scripts/activate```
  2. Initialize the server
  ```bash
  venv/Scripts/activate
  python manage.py runserver
  ```
  By default, the server is initialized to `http://127.0.0.1:8000/`

## Authors
- [Alejandro Medrano](https://github.com/havuh)
- [Rogger Barrientos](https://github.com/RoggerG-hub)
