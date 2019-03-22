from django.shortcuts import render

posts = [
    {
        'author': 'Athena Liu',
        'title': 'Blog 1',
        'content': 'content blog...',
        'date_posted':'9-12-2019'
    },
    {
        'author': 'Athena Liu',
        'title': 'Blog 2',
        'content': 'content blog 2...',
        'date_posted':'9-13-2019'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html',{"title": "About"})