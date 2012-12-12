#!/bin/sh
cd /home/apex/mmqweb/
. bin/activate
PRODUCTION=True gunicorn_django -c gunicorn_conf.py
