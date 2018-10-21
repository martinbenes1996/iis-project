import re

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from kavarna import models

def getSearchBar(d):
    with open('kavarna/templates/searchbar.html', 'r') as searchbar:
        t = Template( searchbar.read() )
        c = Context( d )
    return t.render(c)

def getDrinkerData(email):
    u = models.Drinker.objects.get(email=email)
    if u != None:
        return {'email' : email, 'name' : u.name, 'surname' : u.surname, 
                'fav_coffee' : u.fav_coffee, 'fav_prep' : u.fav_preparation,
                'likes_cafe' : u.likes_cafe}
    else:
        return {}

def userExists(email):
    return u.models.Drinker.objects.get(email=email) != None

def mergeDicts(d1, d2):
    return {**d1, **d2}

def index(request):
    d = dict()
    try:
        email = request.COOKIES['user'] 
        if userExists(email):
            d = mergeDicts( d, getDrinkerData(email) )
        else:
            d['message'] = 'Unknown user'
    except:
        pass

    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)

    d['users_list'] = models.Drinker.objects.all()
    
    return render(request, "index.html", d)

def register(request):
    v = dict()
    v['type'] = 'Register'
    if request.method == 'POST':
        # parse form
        v['name'] = request.POST.get("name", "")
        v['surname'] = request.POST.get("surname", "")
        v['email'] = request.POST.get("email", "")
        v['password'] = request.POST.get("password", "")

        # not matching passwords
        if v['password'] != request.POST.get("password2", ""):
            v['warning'] = '<div class="alert alert-warning" role="alert">Passwords not matching.</div>'
            return render(request, "register.html", v)
        # invalid email
        if re.match(r'.+@.+\..+', v['email']) is None:
            v['warning'] = '<div class="alert alert-warning" role="alert">Invalid email.</div>'
            return render(request, "register.html", v)

        # go to home
        user = User(username=v['email'], password=v['password'])
        drinker = models.Drinker(email=v['email'], name=v['name'],
                    surname=v['surname'])
        user.save()
        drinker.save()
        return redirect('')
    else:
        return render(request, "register.html", v)

def signin(request):
    v = dict()
    v['type'] = 'Signin'
    if request.method == 'POST':
        # parse form
        v['email'] = request.POST.get("email", "")
        v['password'] = request.POST.get("password", "")

        # invalid email
        if re.match(r'.+@.+\..+', v['email']) == None:
            v['warning'] = '<div class="alert alert-warning" role="alert">Invalid email.</div>'
            return render(request, "signin.html", v)

        # go to home
        user = authenticate(username=v['email'], password=v['password'])
        if user is not None:
            response = redirect('')
            response.set_cookie('user', v['email'], max_age=7200)
            return response
        else:
            v['message'] = 'No user with given email'

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
