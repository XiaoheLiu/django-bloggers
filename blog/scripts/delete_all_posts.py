from blog.models import Post


def run():
    '''
    Delete all posts
    $ python manage.py runscript delete_all_posts
    '''
    Post.objects.all().delete()
