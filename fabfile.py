# PYTHON 2 code
from fabric.api import *

prod_server = 'snirp@snirp.webfactional.com'


def prod():
    env.hosts = [prod_server]
    env.remote_app_dir =    '~/webapps/conditie/pressie'
    env.remote_apache_dir = '~/webapps/conditie/apache2'
    env.remote_venv_dir =   '~/webapps/conditie/venv'


def commit():
    message = raw_input("Enter a git commit message:  ")
    local("git add -A && git commit -m \"%s\"" % message)
    local("git push origin master")
    print "Changes have been pushed to remote repository..."


def collectstatic():
    require('hosts', provided_by=[prod])
    with cd(env.remote_app_dir):
        run("python manage.py collectstatic --noinput")


def restart():
    require("hosts", provided_by=[prod])
    require("remote_apache_dir", provided_by=[prod])
    with cd(env.remote_apache_dir):
        # Will not work unless pty is set to False:
        # http://docs.fabfile.org/en/1.4.3/faq.html#init-scripts-don-t-work
        run("bin/restart", pty=False)

def deploy():
    with prefix("source %s/bin/activate" % env.remote_venv_dir):
        with cd(env.remote_app_dir):
            run('git pull origin master')
            run('pip install -r requirements.txt')
            run('python manage.py syncdb')
            run('python manage.py migrate')
        collectstatic()
        restart()
