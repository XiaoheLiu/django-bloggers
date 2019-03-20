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

- Make a basic view in `views.py`
- Create `blog/urls.py` and link views to urlpatterns
- Modify `urls.py` and add the blog app urls to the main urls