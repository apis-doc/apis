import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apis.settings')
django.setup()

from main.models import *


def add_user():
    u, _ = User.objects.get_or_create(username='111111')
    u.set_password('111111')
    u.save()


if __name__ == '__main__':
    add_user()
