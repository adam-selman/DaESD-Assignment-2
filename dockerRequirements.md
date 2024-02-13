# Docker compose requirements 
Once the repository is cloned the django image needs to be built to then run both the mysql and django containers. 
- docker compose build 
- docker compose up -d 
- docker compose down ( clean way for stopping the containers  )
In order to run Django commands while the containers are running the following commands are required . 
## For migrations :
 - docker compose run django  sh - c  “cd /code/SmartCare/ && python manage.py makemigrations  && python manage.py  migrate"
## For testing : 
