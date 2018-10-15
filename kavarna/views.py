import re

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
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
    v = dict()
    v['type'] = 'Register'
    if request.method == 'POST':
        # parse form
        v['name'] = request.POST.get("name", "")
        v['surname'] = request.POST.get("surname", "")
        v['username'] = request.POST.get("username", "")
        v['password'] = request.POST.get("password", "")

        # not matchning passwords
        if v['password'] != request.POST.get("password2", ""):
            v['warning'] = '<div class="alert alert-warning" role="alert">Passwords not matching.</div>'
            return render(request, "register.html", v)
        # invalid email
        if re.match(r'.+@.+\..+', v['username']) is None:
            v['warning'] = '<div class="alert alert-warning" role="alert">Invalid email.</div>'
            return render(request, "register.html", v)
        # user with the email already exists
        #u = models.User.objects.filter(email=v['username'])
        #if models.User.objects.get(email=v['username']) != None:
        #    v['warning'] = '<div class="alert alert-warning" role="alert">User with the email already exists.</div>'
        #    return render(request, "register.html", v)
        
        #u = models.User(email=v['username'],
        #                name=v['name'],
        #                surname=v['surname'],
        #                password=['password'])
        #u.save()

        # go to home
        return redirect('')
    else:
        return render(request, "register.html", v)

def signin(request):
    v = dict()
    v['type'] = 'Signin'
    if request.method == 'POST':
        # parse form
        v['username'] = request.POST.get("username", "")
        v['password'] = request.POST.get("password", "")

        # invalid email
        if re.match(r'.+@.+\..+', v['username']) == None:
            v['warning'] = '<div class="alert alert-warning" role="alert">Invalid email.</div>'
            return render(request, "signin.html", v)

        # go to home
        return redirect('')
    else:
        return render(request, "signin.html", v)

def search(request):

    testOwner = models.Owner(name = "Jan", surname = "Honzik")
    testOwner.save()

    testC = models.Cafe(name = "U Martina", street = "Martinovo namesti", housenumber = 47, city = "Brno", psc = 66600,
                opensAt = "9:00", closesAt = "18:00", capacity = 50, description = "Very nice...", owner = models.Owner.objects.first(),
                )
    testC.save()

    test = models.CoffeeBean(name = "zrnko", origin = "cze", aroma = "nevonne", acidity = 10)
    test.save()
    test2 = models.CoffeeBean(name = "africka namka", origin = "cze", aroma = "nevonne", acidity = 10)
    test2.save()
    test3 = models.CoffeeBean(name = "moje kavicka", origin = "cze", aroma = "nevonne", acidity = 10)
    test3.save()

    d = dict()
    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)
    # cafe results
    objects = models.CoffeeBean.objects.all()
    d['caferesults'] = []
    for bean in objects:
        d['caferesults'].append(bean)
    # coffee results
    objects = models.Cafe.objects.all()
    d['coffeeresults'] = []
    for cafe in objects:
        d['coffeeresults'].append(cafe)
    # coffeebeansresults results

    pom = render(request, "search.html", d)

    models.CoffeeBean.objects.all().delete()
    models.Cafe.objects.all().delete()
    models.Owner.objects.all().delete()
    #test3.delete()

    return pom

# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information
