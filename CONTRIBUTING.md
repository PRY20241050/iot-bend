# Contributing

> Thank you for considering contributing to our project. Your help is very much appreciated!

When contributing, it's better to first discuss the change you wish to make via issue or discussion, or any other method
with the owners of this repository before making a change.

- [Getting started](#getting-started)
  - [Create a virtual environment for the project and initialize](#create-a-virtual-environment-for-the-project-and-initialize)
  - [Environment variables](#environment-variables)
  - [Create an admin superuser](#create-an-admin-superuser)
  - [Prepare and apply data migrations](#prepare-and-apply-data-migrations)
  - [Access the admin panel](#access-the-admin-panel)
- [Pull Request Process](#pull-request-process)

## Getting started

In order to make your contribution please make a fork of the repository. After you've pulled the code, follow these
steps to kick-start the development:

### Create a virtual environment for the project and initialize
  1. Create a virtual environment in the project folder.
  2. Initialize the virtual environment.
  3. Install the project dev dependencies.
      ```bash
      py -m venv venv
      venv/Scripts/activate
      pip install -r requirements/dev.txt
      ```
### Environment variables
Create a .env file in the environments folder with the variables described in the `.env.template` file.

### Create an admin superuser
To modify the website from the admin panel you need to create a superuser. ```python manage.py createsuperuser```

For more information consult [How to create superuser in Django?](https://www.geeksforgeeks.org/how-to-create-superuser-in-django/)

### Prepare and apply data migrations
To apply the migrations to the database you need to execute the following commands.
```bash
python manage.py makemigrations
python manage.py migrate
```

### Access the admin panel
To access the admin panel you need to go to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials.

## Pull Request Process

1. We follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/) in our commit messages, i.e.
   `feat(core): improve typing`
2. Make sure you cover all code changes with unit tests
3. Run ```pre-commit install``` to install pre-commit hooks
4. Make sure all tests pass and there are no linting errors
5. When you are ready, create Pull Request of your fork into original repository
