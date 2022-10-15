#!/bin/sh
cd /home/flask_app/conversorArchivosAudio

exec gunicorn -b :5000 --access-logfile - --error-logfile - wsgi:app
