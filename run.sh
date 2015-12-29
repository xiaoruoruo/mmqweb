#!/bin/sh
cd /home/apex/mmqweb/
. bin/activate
PRODUCTION=TRUE gunicorn mmqweb.wsgi -c gunicorn_conf.py
