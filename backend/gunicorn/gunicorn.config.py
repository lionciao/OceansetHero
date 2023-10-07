import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1

backlog = 2048

worker_class = 'gevent'
proc_name = 'gunicorn.proc'
pidfile = '/tmp/gunicorn.pid'

accesslog = '-'
errorlog = '-'
