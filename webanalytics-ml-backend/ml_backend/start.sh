#!/bin/bash
python manage.py runserver 8001 &
celery -A ml_server worker --beat