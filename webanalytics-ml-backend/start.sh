#!/bin/bash
python ml_backend/manage.py runserver 0.0.0.0:8001 ;
celery -A ml_server worker --beat -l info