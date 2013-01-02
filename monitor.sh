#!/bin/bash
wget --timeout=3 --tries=1 http://127.0.0.1:8557/ -O /dev/null
if [ $? -ne 0 ];then
  PID=$(<"/home/apex/mmqweb/gunicorn.pid")
  echo "Restarting $PID"
  kill -HUP $PID
fi
