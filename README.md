# Project Manager
### Dependencies
* Django 4
* Python 3.11
* Redis last
* DRF last
* Celery last
* Poetry last


## Running project on local machin
Clone project to your computer

    https://github.com/zifrit/NKO.git

Install all dependencies

    poetry install
Run project

    ./manage.py runserver

Swagger 

    http://127.0.0.1:8000/api/schema/swagger/

### Running celery worker machin on a local machin
Need to change the filed in settings.py file\
Before

    CELERY_BROKER_URL = 'redis://redis:6379/0'
After

    CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
Run redis in docker 

    docker  run -p 127.0.0.1:6379:6379 --name redis-celery -d redis
Run worker 

    celery -A NKO worker -l info


## Running project on Docker

Clone project to your computer

    https://github.com/zifrit/NKO.git

Need to change the filed in celery.py, manage.py, wsgi.py files\
Before

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NKO.settings.settings_dev')
After

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NKO.settings.settings_prod')
Run project on docker

    docker compose up --build

Swagger 

    http://0.0.0.0/api/schema/swagger/
