# IoT Monitoring Bend

## Initialize the project locally
### Create a virtual environment for the project and initialize
  1. Execute `py -m venv venv` to create the environment.
  2. Initialize the virtual environment and install the project dependencies.
      ```bash
      venv/Scripts/activate
      pip install -r requirements.txt
      ```
### Environment variables
Create a .env file in the environments folder with the variables described in the `.env.template` file.

### Create an admin superuser
To modify the website from the administration panel you need to create a superuser. ```python manage.py createsuperuser```

For more information consult [How to create superuser in Django?](https://www.geeksforgeeks.org/how-to-create-superuser-in-django/)

### Prepare and apply data migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### To initialize the project you need to start the server to see the changes.
  1. Activate the virtual environment ```venv/Scripts/activate```
  2. Execute 
  ```bash
  python manage.py runserver
  ```
  By default, the server is initialized to `http://127.0.0.1:8000/`
