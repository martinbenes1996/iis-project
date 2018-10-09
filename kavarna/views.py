from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from kavarna import models

def getSearchBar(d):
    with open('kavarna/templates/searchbar.html', 'r') as searchbar:
        t = Template( searchbar.read() )
        c = Context( d )
    return t.render(c)

def index(request):
    d = dict()
    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)
    return render(request, "index.html", d)

def register(request):
    return render(request, "register.html", {})

def signin(request):
    return render(request, "signin.html", {})

def search(request):
    d = dict()
    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)
    # cafe results
    d['caferesults'] = []
    for n in range(1,10):
        u = models.User()
        u.name=str(n)
        d['caferesults'].append(u)
    # coffee results
    d['coffeeresults'] = []
    for n in range(10,20):
        u = models.User()
        u.name=str(n)
        d['coffeeresults'].append(u)
    # place results
    d['placeresults'] = []
    for n in range(20,30):
        u = models.User()
        u.name=str(n)
        d['placeresults'].append(u)
    return render(request, "search.html", d)

# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information