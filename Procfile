release: python manage.py migrate && python manage.py add_site
web: gunicorn eval_project.wsgi  --log-file -
