# Images
This project is an API that allows any user to upload an image in PNG or JPG format.

## Installation

### Poetry
Please note that the project's virtual environment is created with poetry. Install poetry first on **Linux** by using a following command:

```shell
curl -sSL https://install.python-poetry.org | python3
```

Make sure to add poetry to your PATH. To do so, following steps can be taken:

- execute a following command in the terminal to edit `.bashrc` file:
```shell
nano ~/.bashrc
```
- at the bottom of the file place the following line:
```shell
export PATH="/home/<username>/.local/bin:$PATH"
```
- finally execute a command from the file by typing:
```shell
source ~/.bashrc
```
The poetry should be ready to use. For more information regarding the installation of poetry on Linux and other platforms visit a website with [poetry documentation](https://python-poetry.org/docs/).

After installing poetry, activate it. Go to the project's root directory and enter the following command:
```shell
poetry shell
```

The virtual environment is activated. Next you need to make sure that all project's dependencies are installed. In order to do this type:

```shell
poetry install
```

The virtual environment is ready to use.

### Docker

Before you run the server, make sure that you have a docker. To install docker on Linux execute a following command in the terminal:

```shell
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Enable your user to properly use the docker commands without using sudo for every command. Execute the following command and then reboot the system:

```shell
sudo usermod -aG docker <username>
```
After rebooting a system, you should see `docker` as a new user in groups. It means that docker is ready to use. Execute a following command in the terminal to start the database (the command can be different on other operational systems):

```shell
docker compose up
```

For more information regarding the installation of docker on Linux and other platforms visit a website with [docker documentation](https://docs.docker.com/engine/install/).

## Starting the server

When the virtual environment as well as database are ready to user, you can start the server. In order to start the server run migration first:

```shell
python manage.py migrate
```

and then start the server:

```shell
python manage.py runserver
```

You can also start the django project with gunicorn server:
```shel
gunicorn images.wsgi -w 10
```
`10` stands for number of workers I can add to the server so that it enhances the performance of the server in case there are more calls to api. The number can be changed.

## The content of the project:

### The following urls are available on the server:

- http://127.0.0.1:8000/admin/ - a link to administration site
- http://127.0.0.1:8000/api/upload-image/ - a link to upload images for a logged-in users
- http://127.0.0.1:8000/api/images/ - a link to uploaded images for a logged-in user
- http://127.0.0.1:8000/api/create-link/ - a link to create an expiring link by an authorized user
- http://127.0.0.1:8000/api/expiring-links/ - a link to expiring link for an authorized user

### There are also 4 built-in users:

- username: image / password: image1234! - superuser with no account tier:

- username: basic / password: basic1234! - stuff user with basic account tier:

- username: premium / password: premium1234! - stuff user with premium account tier:

- username: enterprise / password: enterprise1234! - stuff user with enterprise account tier:
