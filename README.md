# Lets-Play
Django based app for showing the list of the CS servers within the IIT-R campus

![final1](https://cloud.githubusercontent.com/assets/10174820/12300679/9b145f62-ba42-11e5-892a-c1f94c885250.png)


## Setup
1. Install Python2, Django==1.7.8 and mysql-python (preferably in a virtual env).
2. Create a new DB in mysql and a new user having full access to that DB.
3. Copy LPapp/configuration.py.sample to LPapp/configuration.py provide the DB and user details.
4. Run ./manage.py migrate.
5. Run ./manage.py runserver
6. Run by using python manage.py runserver --noreload --insecure ip:port
