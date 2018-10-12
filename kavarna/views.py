from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from . import models
from .models import CoffeeBean

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
    # test = Cafe(name = "U Martina", street = "Martinovo namesti", housenumber = 47, city = "Brno", psc = 66600,
    #             opensAt = "9:00", closesAt = "18:00", capacity = 50, description = "Very nice...", )
    test = CoffeeBean(name = "zrnko", origin = "cze", aroma = "nevonne", acidity = 10)
    test.save()
    test2 = CoffeeBean(name = "africka namka", origin = "cze", aroma = "nevonne", acidity = 10)
    test2.save()
    test3 = CoffeeBean(name = "moje kavicka", origin = "cze", aroma = "nevonne", acidity = 10)
    test3.save()

    d = dict()
    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)
    # cafe results
    objects = CoffeeBean.objects.all()
    d['caferesults'] = []
    #d['caferesults'] = []
    #for n in range(1,10):
    for bean in objects:
        d['caferesults'].append(bean)
        #u = models.User()
        #u.name=str(n)
        #d['caferesults'].append(u)
    # coffee results
    d['coffeeresults'] = []
    for n in range(10,20):
        u = models.User()
        u.name=str(n)
        d['coffeeresults'].append(u)
    # coffeebeansresults results




    pom = render(request, "search.html", d)

    CoffeeBean.objects.all().delete()
    #test.delete()
    #test2.delete()
    #test3.delete()

    return pom

# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information
