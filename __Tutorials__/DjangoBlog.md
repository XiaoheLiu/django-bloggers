## 1. Getting Started

### Setting Up Virtual Environment
Initiate the virtual environment and activate it:
```bash
python3 -m venv django_env
source django_env/bin/activate
```

Install packages and check version:
```bash
python -m pip install --upgrade pip
pip3 install django
# Must use pip3!
python -m django --version
```

Generate/update requirements.txt file:
```bash
pip freeze > requirements.txt
```

To install the packages specified in requirements.txt:
```bash
 pip install -r requirements.txt
```

### Start the project
```bash
django-admin startproject django_project
cd django_project/
python manage.py runserver
```

## 2. Routing

Create an application
```bash
python manage.py startapp blog
```
- Add the blog app to project settings: in `settings.py` add `blog.apps.BlogConfig` to the "installed apps" list
- Make a basic view in `views.py`
- Create `/blog/urls.py` and link views to urlpatterns:
`
path('', views.home, name='blog-home'),
`
- Modify `/urls.py` and add the blog app urls to the main urls

## 3. Templates
- Create `/blog/templates/blog` folder and add `templateName.html`
- Render the html in `views.py`
- Pass data as objects to templates through the 3rd arg in `render(request, 'blog/home.html', context)`, and refer to data in the templates using the jinja, eg. `{{ posts[0].author }}`. 
- Use template inheritance to avoid duplicated template code. (use `block` in base.html, and add "children" by using `extends`)
- Add css: create `blog/static/blog/styles/main.css`; in the `base.html`, add the statics using `load static` at above and link the stylesheet. (Need to restart server for the static files to be loaded)
- Use programmable url in base.html by calling `href="{% url 'blog-home' %}`