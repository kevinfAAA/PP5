from django.shortcuts import render, redirect

# landing page view


def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def handler404(request,*args,**argv):
    return render(request, 'home/404.html')
