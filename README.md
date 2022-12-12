# Mosques-Near-Me
### AWM 2022/23 Assignment 2
### Progressive Web Mosque Locator App

Mosques Near Me is a Django PWA which finds and locates nearby mosques to the users current location. The user can add mosques to a list containing their favourite mosques and they can display the route a mosque that they click on.  

## What is included in this project:
- A Django PWA
- 3 local docker containers which communicate on the same network:
    1. Postgis - spatial DB
    2. Pgadmin4 - for database management
    3. mosque_app - containing Django project

The external libraries used for this project can be found in the ENV.yml file. Project was developed in a conda environment

## Mosque App
### Html files (Templates)
  - A sign-up page which allows new users to register
  - A login page which allows existing users to login
  - A menu page which displays what services are available to the user
  - A map page which displays a map and plots the users current location with a little pop-up message containing their location (map is generated using leafletJs), local mosques are marked using a purple circle marker and route is displayed when marker is pressed
  
### Models
 - World borders model containing geodjango data 
 - User profile model which uses a one-to-one link to extend the Django auth User model. User profile now includes a userlocation column to store location data
 - Mosque model which contains the users favourite mosques with a foreign key of user
   
### Views
 - A register view which is connected to the registration form when a new user is registered
 - A login view which is conneted to the login form
 - A update_location view which updates the location data in the database. Location is updated via an ajax request passed whenever the map page is open
 All forms are generated using crispy forms
 - A findmosque view which returns a geojson object after processing a overpass query to find mosques
 
 ## UI of Mosques Near Me
 PWA installed as app on laptop:
 ![Screenshot_20221211_232649](https://user-images.githubusercontent.com/57072598/206944171-981cd4d0-58c3-4272-939d-f3cea13c50c6.png)

 Landing page in PWA:
 ![Screenshot_20221211_232422](https://user-images.githubusercontent.com/57072598/206944133-699d3dd5-b99f-48a2-9ccc-6053ab8e6c8f.png)
 
 Map page in PWA:
 ![image](https://user-images.githubusercontent.com/57072598/206945297-28d89b77-7727-458c-b5c8-ae2c44da3b6f.png)

Displaying multiple Mosques with purple markers:
![multiple-mosques](https://user-images.githubusercontent.com/57072598/206944284-015b37d4-9c6f-465d-858c-4fe1438ca022.jpg)

 Displaying route to mosque:
 ![route-to-mosque](https://user-images.githubusercontent.com/57072598/206944341-cdf459c5-63a0-48db-8eb6-d881552f0283.jpg)

 Favourite Mosques in the database:
![image](https://user-images.githubusercontent.com/57072598/207154562-8cf648cb-7be7-4c38-9e7d-a6a2a81f2fde.png)


Plotting users favourite mosque in Django Admin website:
![image](https://user-images.githubusercontent.com/57072598/206944990-dddcd6a4-a7e5-4f21-a4fd-eedd3ce1925c.png)

 ## Deployment
- Created a DigitalOcean droplet that had docker preinstalled
- Aquired a domain name (wedaadharuna.online)
- Unfortuantely deployment of this project was unsuccessful. Due to the following:
![image](https://user-images.githubusercontent.com/57072598/206943980-1c52d93f-745e-4595-b207-92f3fa3d0266.png)



