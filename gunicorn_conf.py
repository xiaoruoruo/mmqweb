# run with: bin/gunicorn_django -c gunicorn_conf.py
bind = '0.0.0.0:8557'
workers = 4
accesslog = 'data/access.log'
access_log_format = '%({X-Real-IP}i)s %(l)s %(u)s %(t)s %(D)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s'
pidfile = 'gunicorn.pid'
forwarded_allow_ips = '*'
