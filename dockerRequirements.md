# 1. Docker compose requirements 

- [1. Docker compose requirements](#1-docker-compose-requirements)
  - [1.1. Initial Container Setup](#11-initial-container-setup)
  - [1.2. Running Django Application](#12-running-django-application)
    - [1.2.1. For migrations](#121-for-migrations)
    - [1.2.2. For testing](#122-for-testing)
      - [1.2.2.1. Running the Server](#1221-running-the-server)
      - [1.2.2.2. Adding Dummy Data](#1222-adding-dummy-data)



Once the repository is cloned the django image needs to be built to then run both the mysql and django containers. 

## 1.1. Initial Container Setup

```bash
docker compose build 
```

```bash
docker compose up -d 
```

```bash
docker compose down
```
The above is a clean way for stopping the containers.

## 1.2. Running Django Application

In order to run Django commands while the containers are running the following commands are required.

### 1.2.1. For migrations

 - Open a terminal and navigate to the `DESD_2024` directory of the repo and then run the following commands:

```bash
docker compose run django  sh - c  "cd /code/SmartCare/ && python manage.py makemigrations  && python manage.py  migrate"
```

```bash
docker compose run django sh -c "cd /code/SmartCare/ && python rebuild.py"
```
### 1.2.2. For testing

#### 1.2.2.1. Running the Server

```bash
docker compose run django  sh -c  "cd /code/SmartCare/ && python manage.py runserver"
```

#### 1.2.2.2. Adding Dummy Data
