#!/bin/bash
python manage.py runserver 8002 &
celery -A server worker --beat