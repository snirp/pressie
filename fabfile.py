# PYTHON 2 code

from fabric.api import *


def commit():
    message = raw_input("Enter a git commit message:  ")
    local("git add -A && git commit -m \"%s\"" % message)
    local("git push origin master")
    print "Changes have been pushed to remote repository..."




def deploy():
    env.hosts = 'snirp@snirp.webfactional.com'
    project_dir = '~/webapps/conditie'
    django_dir = project_dir + '/pressie'
    with prefix('source ~/webapps/conditie/venv/bin/activate'):
        with cd(django_dir):
            run('eval $(ssh-agent)')
            run('ssh-add ~/.ssh/id_rsa')
            run('git pull origin master')
            run('pip install -r requirements.txt')
            run('python manage.py syncdb')
            run('python manage.py migrate')
            run('python manage.py collectstatic --noinput')
        with cd(project_dir):
            run('apache2/bin/restart')
