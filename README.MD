# Best taxi ever

Django project for for managing cars, manufacturers and drivers.

## Check it out
Link on render -> Will be soon

## Installation:


```sh
git clone https://github.com/IvanStored/best-taxi-ever.git
cd best-taxi-ever
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata taxi_service_db_data.json
python manage.py runserver  # starts Django project
```

## Features:
- Authentication functionality for Driver/User
- Managing drivers, cars, manufacturers directly from website
- Registration for new Drivers/Users
- Rating system for cars and drivers (using django-star-rating)
- User can upload own avatar
- Feedback form

## In future(maybe):
- Direct messages for users
- Comment system for cars

# Demo:
## Home page
![img.png](img.png)

## Car list
![img_1.png](img_1.png)
## Manufacturer list
![img_2.png](img_2.png)
## Driver list
![img_3.png](img_3.png)
## Driver profile
![img_4.png](img_4.png)
## Car information
![img_5.png](img_5.png)
## Manufacturer information
![img_6.png](img_6.png)
## Feedback form
![img_7.png](img_7.png)
## Success 
![img_8.png](img_8.png)
## Error message
![img_9.png](img_9.png)