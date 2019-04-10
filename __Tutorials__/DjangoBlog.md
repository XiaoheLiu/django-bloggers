# Django Blog

## 1. Getting Started

### Setting Up Virtual Environment

- Initiate the virtual environment and activate it:

```bash
python3 -m venv django_env
source django_env/bin/activate
```

- Install packages and check version:

```bash
python -m pip install --upgrade pip
pip3 install django
# Must use pip3!
python -m django --version
```

- Generate/update requirements.txt file:

```bash
pip freeze > requirements.txt
```

- To install the packages specified in requirements.txt:

```bash
 pip install -r requirements.txt
```

- Now start the project

```bash
django-admin startproject django_project
cd django_project/
python manage.py runserver
```

## 2. Routing

- Create an application

```bash
python manage.py startapp blog
```

- Add the blog app to project settings: in `settings.py` add `blog.apps.BlogConfig` to the "installed apps" list
- Make a basic view in `views.py`
- Create `/blog/urls.py` and link views to urlpatterns:
  `path('', views.home, name='blog-home'),`
- Modify `/urls.py` and add the blog app urls to the main urls

## 3. Templates

- Create `/blog/templates/blog` folder and add `templateName.html`
- Render the html in `views.py`
- Pass data as objects to templates through the 3rd arg in `render(request, 'blog/home.html', context)`, and refer to data in the templates using the jinja, eg. `{{ posts[0].author }}`.
- Use template inheritance to avoid duplicated template code. (use `block` in base.html, and add "children" by using `extends`)
- Add css: create `blog/static/blog/styles/main.css`; in the `base.html`, add the statics using `load static` at above and link the stylesheet. (Need to restart server for the static files to be loaded)
- Use programmable url in base.html by calling `href="{% url 'blog-home' %}`

## 4. Django Admin Page

```bash
# First, detect changes in database and update
python manage.py makemigrations
# Next, apply the migration
python manage.py migrate
python manage.py createsuperuser
# Restart the server to login
```

## 5. Database and Migrations

- ORM: Object Relational Mapper
- Represent data structure in python classes (models)
- It is possible to use SQLite in development, and Postgres for production. You just need to change the settings.
- In `blog/models.py`, create `class Post(models.Model):`, then make migrations.
- Django generated a `blog/migrations/0001_initial.py` file.
- To view the sql code that django is going to run

```bash
python manage.py sqlmigrate <app_name> <migration_id>
python manage.py sqlmigrate blog 0001
```

- Migrate: `python manage.py migrate`
- We can query the database using django shell interactively. `python manage.py shell`

```python
from blog.models import Post
from django.contrib.auth.models import User
User.objects.all()
User.objects.first()
User.objects.last()
user = User.objects.filter(username='athena').first()
user.id
user.pk # primary key
user2 = User.objects.get(id=2)
# Create a post and save to database
post_1 = Post(title='Blog1', content='ipsi lorem', author=user)
post_1.save()
post_2 = Post(title='Blog2', content='ipsi2 lorem2', author_id=user2.id)
post_2.save()
Post.objects.all()
# Get all the posts written by one user
user.post_set.all()
# Let this user create a post
user.post_set.create(title='Blog3', content='ipsi3 lorem3')
```

- In `views.py`, query the data from database instead of using the dummy data: `from .models import Post`, then `Post.objects.all()`
- In the `home.html` template, use the django [date formatter (filter)](https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#date) to display date: `{{ post.date_posted|date:"F d, Y" }}`
- To access the new Post model through admin page, register it by importing Post and then adding `admin.site.register(Post)` to `blog/admin.py`

# 6. User Registration Page

- Create an app for handling users: `python manage.py startapp users`, and register it in `settings.py`.
- In `views.py`, create a default register form by importing django's default form `from django.contrib.auth.forms import UserCreationForm`
- Create the template `register.html`. Load the form as paragraphs by `{{ form.as_p }}`
- Link the url directly to the project `urls.py`
- Handle form submissions:
  - Alert using a one time message `from django.contrib.messages import messages` (This will be sent to the template)
    - Types include: messages.debug/info/success/warning/error
    - Display the message in `base.html`
  - Redirect to another page `from django.shortcuts import redirect`, then `return redirect('blog-home')`
  - Create "email" field by making a form class that inherits the UserCreationForm class. See `users/forms.py`
- Install 3rd party package: `crispyforms` to make the form look better
  - `pip install django-crispy-forms`
  - In `settings.py`, add to installed apps: `'crispy_forms'` and also specify to use Bootstrap4 `CRISPY_TEMPLATE_PACK = 'bootstrap4'`
  - Add to template: `{% load crispy_forms_tags %}` then use pipe filter `{{ form|crispy}}`

# 7. Login and Logout Page

- In the project url.py, import class based auth views `from django.contrib.auth import views as auth_views` and include them in the url patterns: `path('login/', auth_views.LoginView.as_view(), name='login'),`
- Create login template
- Change redirect url setting in `settings.py` by `LOGIN_REDIRECT_URL = 'blog-home'`
- Update the `base.html` to link to the login/logout urls. Conditionally show the links. `{% if user.is_authenticated %}`
- Create a user profile page. view ➡️ urls ➡️ template.
- Add function decorator to the profile view. To import: `from django.contrib.auth.decorators import login_required`. This acts like a middleware. Now if the user is not logged in and hit the profile url, they will be redirected to the login page, and once they logged in, they will be redirected back to the profile page.
- By default, django puts login url at `/accounts/login`, but we can change that in settings by `LOGIN_URL = 'login'`

# 8. User Profile and Picture

- Create a Profile model that extends from the default django User model in `/users/models.py`
- `pip install Pillow` to be able to deal with images
- Make migration, then migrate in the CLI.
- Register the Profile model in the admin page in `/users/admin.py`. Now create a user profile in admin page.
- Go to django shell and inspect on the image:

```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.filter(username='athena').first()
>>> user
<User: athena>
>>> user.profile
<Profile: athena Profile>
>>> user.profile.image
<ImageFieldFile: profile_pics/A_ORIGAMI.JPEG>
>>> user.profile.image.width
3024
>>> user.profile.image.url
'profile_pics/A_ORIGAMI.JPEG'
```

- The images are currently saved in `/profile-pics`. Not convenient. Let's change it to save in `/media/profile-pics`. In `settings.py`, add `MEDIA_ROOT = os.path.join(BASE_DIR, 'media')` and also `MEDIA_URL = '/media/'` (where the pics will be accessed through website)
- Serve uploaded files from media folder in development, check the [official doc](https://docs.djangoproject.com/en/2.1/howto/static-files/#serving-files-uploaded-by-a-user-during-development). For production, check [the doc](https://docs.djangoproject.com/en/2.1/howto/static-files/deployment/)
- Put a default.jpg into /media folder.
- Want a user profile to be created when a new user registered. Make a `signals.py` and add a `create_profile` signal and a `save_profile` signal. Then register the signals in the apps.py.

# 9. User Profile Update

- Create `UserUpdateForm` and `ProfileUpdateForm` in `users/forms.py`
- Import the forms in `users/views.py`
  - Initiate a new instance of the forms, and pass to the template as context.
  - Populate current user information in the profile view `SomeForm(instance=request.someModel)`
  - User if statements to handle POST request and save form and redirect if forms are valid
- Add the form to `profile.html` template. Remember to add `enctype="multipart/form-data"` attribute to the form tag for handling images.
- To resize the profile image and save a smaller one, in `users/models.py`:
  - Use the Pillow package for resizing: `from PIL import Image`.
  - Override the save method of Profile model.
- Include author's profile picture by the side of their article.

# 10. Full CRUD Features for Posts

### ListView

- Create PostListView (a class based view) at `blog/views.py` and import it in `blog/urls.py`
- By default, ListView looks for a template at `<app>/<model>_<viewType>.html`, in this case `blog/post_list.html`. Also, the variable passed to the template is `<model>_<viewtype>`, eg. `post_list`. But we can overwrite them by setting `template_name` and `context_object_name`
- To make the latest post on top: `ordering = ['-date_posted']`

### DetailView

- Create PostDetailView, set model to be Post
- Make url patterns. `path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),`
- Create template `post_detail.html`. By convention, refer to the post by `object`
- Update links in the post_list template. `href="{% url 'post-detail' post.id%}"` (post.id) is the parameter taken.

### Create View

- Create the view. Set the fields in the form by `fields = ['title', 'content']`
- Url pattern: `path('post/new', PostCreateView.as_view(), name='post-create')`
- Template share with the update form, named `post_form.html`. Refer to the form element as `form`
- Set author as logged in user by overriding the default `form_valid(self, form)` method
- When form successfully submitted, redirect user to the post-detail page. In `models.py`, set a `get_absolute_url` method for the Post model.
- To protect the new post route from unlogged-in users, make this view inherite from the `LoginRequiredMixin` from `django.contrib.auth.mixins`

### Update View

- Create view. Very similar to the create view.
- Set up url patterns. Use `path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),`
- Only allow the author to update their post. Use `UserPassesTestMixin` and define a `test_func` that returns True if user is the author.

### Delete View

- Create view, inherit from the two mixins and add teh test_func method.
- Set up url patterns `path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),`
- Create `post_confirm_delete.html` template, a form that asks the user to confirm the deletion.
- Add success url to view: `success_url = reverse_lazy('blog-home')`

- Add links in the nav bar and the post detail page.

# 11. Pagination

- Load fake data

```python
$ python manage.py shell
import json
from blogs.models import Post
with open('post.json') as f:
    posts_json = json.load(f)
for post in posts_json:
    post = Post(title=post['title'], content=post['content'], author_id=post['user_id'])
    post.save()
```

- Play with django's paginator object within shell:

```python
from django.core.paginator import Paginator
posts = ['a', 'b', 'c', '1', '2', '3']
p = Paginator(posts, 3)
p.num_pages
for page in p.page_range:
    print(page)
p1 = p.page(1) # <Page 1 of 2>
p1.number # 1
p1.object_list # ['a', 'b', 'c']
p1.has_previous() # False
p1.has_next() # True
p1.next_page_number() # 2
```

- Add pagination in `PostListView` by adding `paginate_by = 2`
- Add links to pages in `home.html`. Page object is referred to as `page_obj`

### Filter Posts by User

- Create `UserPostListView` in `views.py`
- Create url patterns
- Create template `user_posts.html`. Refer to the user in the query parameters by `{{ view.kwargs.username }}`

# 12. Email and Password Reset

- In `urls.py`, set up urls for the
  - _password reset view_ (form to enter email)
  - _password reset done view_ (info display)
  - _password reset confirm view_ (form to enter new password)
  - _password reset complete view_ (message to tell you password is successfully reset):
  - from the `auth_views.PasswordResetView`
- Create templates for these views.

# 13. Set up AWS S3 for File Uploads

- Create S3 bucket
- Create IAM User
- `pip install boto3` and `django-storages` and add `'storages` to the installed apps in settings.py.
- Put ASW related variables into settings.
- Remove the image resizing functionality with pillow in `users/models.py`

# 14. Deploy to Heroku
```bash
heroku create django-bloggers
git push heroku master
heroku logs --tail
heroku config:set SECRETE_KEY="blablabla"
```

- Add `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')` to settings.py to set up static root.
- Add Procfile
- Add herokuapp.com to ALLOWED_HOSTS in settings.py
- Regenerate secret key with `import secrets` `secrets.token_hex(24)` and store it safely in environment variables


- `pip install django-heroku`
- In settings.py, import `django_heroku` and add `django_heroku.settings(locals())` at the bottom
- `heroku run python ./django_progect/manage.py migrate`