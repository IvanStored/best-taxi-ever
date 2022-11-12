# Best taxi ever

Django project for for managing cars, manufacturers and drivers.

## Check it out
Link on render -> [Let`s try!](https://best-taxi-ever.onrender.com)

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
- Direct messages for users

## In future(maybe):
- Comment system for cars

## Bugs:
- User avatar is not displayed

# Demo:
## Home page
![image](https://user-images.githubusercontent.com/43565760/201485185-ffa8a232-b7f3-4b06-be25-f3265a459358.png)

## Car list
![image](https://user-images.githubusercontent.com/43565760/201485232-7abfa028-133f-497f-965e-91b265fd16ac.png)

## Manufacturer list
![image](https://user-images.githubusercontent.com/43565760/201485245-32686b58-7ba0-4a41-b5a4-1f746c7522a9.png)

## Driver list
![image](https://user-images.githubusercontent.com/43565760/201485254-6c802d50-a46f-49bf-b4f0-90543b690e09.png)

## Driver profile(Staff)
![image](https://user-images.githubusercontent.com/43565760/201485281-3a8520fd-ca99-4c75-81b9-56fe054ab83e.png)
![image](https://user-images.githubusercontent.com/43565760/201485312-60f83ae2-92bb-43b3-bf8d-f9dc9937ecfd.png)

## Driver profile(User)
![image](https://user-images.githubusercontent.com/43565760/201485530-9edfc75c-eabb-490f-a6e7-840788175e41.png)

## Manufacturer information
![image](https://user-images.githubusercontent.com/43565760/201485543-8611169b-bff2-407c-937e-94d55f4f299f.png)
## Feedback form
![image](https://user-images.githubusercontent.com/43565760/201485552-17783a80-e763-4a39-8031-c2c51bf7a1b2.png)
## Success 
![image](https://user-images.githubusercontent.com/43565760/201485579-a5559cf5-70fa-46ca-ab93-9381f9e5a72d.png)
## Error message
![image](https://user-images.githubusercontent.com/43565760/201485608-5657d8c6-146a-499b-ae59-7638ab2ad9ce.png)

## Car detail
![image](https://user-images.githubusercontent.com/43565760/201485636-38ecf86b-0616-4361-a248-907cb7401582.png)
