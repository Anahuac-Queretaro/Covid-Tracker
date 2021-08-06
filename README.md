# Covid-Tracker

Repository for a tool that will help tracking the Covid-19 spread in the school

## How to contribute?
To develop you'll have 2 options: **use docker** or **use your own virtual environment**, both are ok.
After cloning your repo, follow the steps bellow.

### Clone the repository
You have to make sure you have already set your SSH keys for your github account.
After that you can start cloning your repository. 

```
git clone git@github.com:Anahuac-Queretaro/Covid-Tracker.git 
```

## Run development environment with docker (recommended)

```
# Build the services
docker compose build

# lift the containers
docker compose up -d
```

And done, you will have running django on `127.0.0.1:8000`

### Develop
To run django and python commands you'll have to enter the containers like this:
```
# Enter sh shell
docker compose exec app sh
```
This will open you the "sh" shell on the container and you will be able to run your python commands like this:

```
# Running migrations example
python manage.py migrate
```

## Run development environment without docker
If you prefer, you can use your own virtual environment, just make sure the version of python you are running is **3.7** to avoid conflicts with your peers.

### Create virtual env
To create a virtual env you can do it as follows:

```
# Create virtual env and choose the name of the folder where it will live.
# e.g. "python3 -m venv .env"
python3 -m venv [.env|env|.venv|env|ENV]

# Activate virtual env
# e.g. "source ./.env/bin/activate"
source ./[name of folder]/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```
### Set env variables
Before running the application you will need a .env file with your local variables.
You can copy the contents of .env.example.
```
# Enter django app folder
cd app

# Create .env file
cp .env.example .env
```
Ask your administrator for _SECRET_KEY_ value.

### Run migrations
Django works with migrations for database control, so you'll need to run them.
```
python manage.py migrate
```

### Run app

```
python manage.py runserver 0.0.0.0:8000
```

