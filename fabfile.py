from fabric.api import *


def deploy():
    project_dir = '~/webapps/conditie'
    django_dir = project_dir + '/pressie'
    with prefix('source ~/webapps/conditie/venv/bin/activate'):
        with cd(django_dir):
            run('git pull origin master')
            run('pip install -r requirements.txt')
            run('python manage.py syncdb')
            run('python manage.py migrate')
            run('python manage.py collectstatic --noinput')
        with cd(project_dir):
            run('apache2/bin/restart')
