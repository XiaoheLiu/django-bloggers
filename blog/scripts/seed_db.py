import json
from blog.models import Post
from datetime import timedelta
from django.utils import timezone
from random import randint


def run():
    '''
    Seed data base with posts read from json file.
    $ pip install django-extensions
    Add django-extensions to installed_apps in settings.
    $ python manage.py runscript seed_db
    '''
    with open('./blog/scripts/posts.json') as f:
        posts_json = json.load(f)
    for post in posts_json:
        post_date = timezone.now() - timedelta(weeks=randint(0, 48))
        post = Post(title=post['title'],
                    content=post['content'], author_id=post['user_id'], date_posted=post_date)
        post.save()
