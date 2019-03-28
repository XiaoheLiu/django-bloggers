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
