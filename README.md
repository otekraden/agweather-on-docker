## AGWeather == Aggregator of the Weather Forecasts 

This web application was built in Python using Django framework.
It has been deployed on VPS server (Ubuntu 20.04) from the Docker Container.
You are welcome to visit it by link: http://agweather.ru/

      
## The Project Idea
At this point, this project was created for only educational purposes as a portfolio project.
The idea of the project came to me with the following question:

>_What happens if to save the weather forecast data and then compare it with the actual weather that has occurred?_

Thus, it will be possible to graphically evaluate which of the services is most accurate in certain conditions.

![agw_screenshot](https://github.com/OtekvonSoraden/agweather-on-docker/assets/92234377/5c92da64-7f44-44f8-8dea-67ea6213603d)

## How does it works?

### This Django project consist of the two apps: <br/>

At the moment, Both are temporary in the "backend" folder.

#### 1. Datascraper

This is the backend part, which responsible for parsing and saving weather information to the database.

On working server crontab is configured to run periodic tasks:

- Every 15 minutes runs management command "run_datascraper" to refresh data from sources
- Every 12 hours runs management command "dump_data_to_ydsk" to save database dump in cloud

#### 2. Website

It is frontend part, which built using Django templates system, DTL (Dlango Template Language) and Bootstrap frontend toolkit.
Interactive graphical data representation realized with Chart.js charting library.

I'am planning to remake this app with Django REST & Vue.js frameworks. So there will be separate 'frontend' folder with its own Dockerfile.

## How to run project on your local machine?

I have written brief instruction how to do it from Docker containers. 
Follow all the steps below and launch the app yourself!

1) Since Docker technology is used here, it doesn't matter which operating system is used, but just in case, I'm clarifying: _Ubuntu 20.04_ \
Launch OS in terminal.

2) At first you need installed Docker vs Docker-compose. Check their installations: \
_docker --version && docker-compose --version_ \
I have: _Docker version 25.0.3, Docker Compose version v2.24.6_ \
If you need installation, see here: https://docs.docker.com/engine/install/

3) Clone repository by command: \
_git clone_ https://github.com/OtekvonSoraden/agweather-on-docker.git

4) Go to folder: _cd agweather-on-docker/infra/staging/_

5) Open _template_env.txt_ file and edit it by inside instructions.
Save it as ".env"

6) To launch containers, run command:
 _docker-compose up -d_

![agw_screenshot1](https://github.com/OtekvonSoraden/agweather-on-docker/assets/92234377/5a5c1179-3e9c-408e-a5b5-b3b2542e779c)


8) If everything Ok, all containers have been started, you can visit our web-application by link: http://localhost:80 \
Default superuser is *'admin'* with the password *"wYuA*v3C9AaX"*.  \
Log in and have fun! :smile:

9) Finally, to start collecting weather data, your need to tune crontab. \
Open file _crontab_e.txt_ and copy all the contents. \
Run command: _crontab -e_ \
Insert insert copied to the end, save and exit file. \
Check *cron* is running: _sudo service cron status_


## Stack of Used Technologies

- Django
- Bootstrap
- Chart.js
- Beautifulsoup
- Selenium
- PostgreSQL
- Linux Ubuntu
- Docker

## TODO List

Possible ways to expand the project. Feel free to write pull requests! ))

1. Add tracked weather parameters. Now there are only 3 of them (temperature, pressure, wind speed). Think about their graphical representation.
2. Add forecast/archive sources. You need to write new scraper classes.
3. Now to check forecasts accuracy possible only graphically. But is it possible to measure it in digitals? I suppose that three need to be some statistics functionality...
4. I am leaning now Django REST & Vue.js frameworks. Have in idea to remake frontend part with this technologies

## Conclusion

This is my very first web application created from scratch. So far, there is very limited functionality here. But in my opinion, I managed to create a scalable data parsing system that can be applied in many information fields.

I will be grateful for any criticism and suggestions. Write me here in GitHub, on the website in the Feedback section or by e-mail agweather@yandex.ru
