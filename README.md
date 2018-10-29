# Fee Management System


Installation:

    sudo pip3 install -r requirement.txt
    
Install MailCatcher:
    
     apt install build-essential libsqlite3-dev ruby-dev
     
       

Run Celery server:

    sudo systemctl enable rabbitmq-server
    
    sudo systemctl start rabbitmq-server
    
    sudo systemctl status rabbitmq-server


Run Celery Worker:

    celery -A vhc_project worker --loglevel=info

Run Django-celery Worker:

    python manage.py celeryd --verbosity=2 --loglevel=DEBUG

Run django-celery-beat:

    python manage.py celerybeat --verbosity=2 --loglevel=DEBUG
