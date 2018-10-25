import re

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context, Template
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import IntegrityError

from kavarna import models

def getSearchBar(d):
    with open('kavarna/templates/searchbar.html', 'r') as searchbar:
        t = Template( searchbar.read() )
        c = Context( d )
    return t.render(c)

def getDrinkerData(email):
    u = User.objects.get(email=email)
    if u != None:
        d = models.Drinker.objects.get(key=u.pk)
        return {'email' : u.email, 'name' : u.first_name, 'surname' : u.last_name,
                'pk' : u.pk,
                'fav_coffee' : d.fav_coffee, 'fav_prep' : d.fav_preparation,
                'likes_cafe' : d.likes_cafe}
    else:
        return {}

def userExists(email):
    return User.objects.get(email=email) != None

def logout(request=None):
    response = redirect('')
    response.delete_cookie('user')
    return response
def errLogout(request, d):
    response = render(request, 'index.html', d)
    response.delete_cookie('user')
    return response

def generateDict(request):
    try:
        email = request.COOKIES['user']
        if userExists(email):
            return getDrinkerData(email)
        else:
            return {'message' : 'Unknown user'}
    except:
        print('Logged: nobody')
        return dict()

def index(request):
    #models.Drinker.objects.all().delete()
    #User.objects.all().delete()
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)
    return render(request, "index.html", d)


def register(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    d['type'] = 'Register'
    if request.method == 'POST':
        # parse form
        d['register_first_name'] = request.POST.get("first_name", "")
        d['register_last_name'] = request.POST.get("last_name", "")
        d['register_email'] = request.POST.get("email", "")
        d['password'] = request.POST.get("password", "")

        # not matching passwords
        if d['password'] != request.POST.get("password2", ""):
            d['warning'] = '<div class="alert alert-warning" role="alert">Passwords not matching.</div>'
            return render(request, "register.html", d)
        # invalid email
        #if re.match(r'.+@.+\..+', d['email']) is None:
        #    d['warning'] = '<div class="alert alert-warning" role="alert">Invalid email.</div>'
        #    return render(request, "register.html", d)
        try:
            user = User.objects.create_user(d['register_email'], password=d['password'])
        except IntegrityError:
            return render(request, "register.html", d)
        user.email = d['register_email']
        user.first_name = d['register_first_name']
        user.last_name = d['register_last_name']
        user.save()
        drinker = models.Drinker(key=user.pk)
        drinker.save()
        return redirect('')

    else:
        return render(request, "register.html", d)

def signin(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    d['type'] = 'Signin'
    if request.method == 'POST':
        # parse form
        d['email'] = request.POST.get("email", "")
        d['password'] = request.POST.get("password", "")

        # invalid email
        #if re.match(r'.+@.+\..+', v['email']) == None:
        #    v['warning'] = '<div class="alert alert-warning" role="alert">Invalid email.</div>'
        #    return render(request, "signin.html", v)

        # go to home
        user = authenticate(username=d['email'], password=d['password'])
        if user is not None:
            response = redirect('')
            response.set_cookie('user', d['email'], max_age=7200)
            return response
        else:
            d['message'] = 'No user with given email'

    return render(request, "signin.html", d)

def search(request):

    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)

    # cafe results
    try:
        d['caferesults'] = models.CoffeeBean.objects.filter(name=d['key']).values()
    except:
        pass
    # ...

    # coffee results
    try:
        d['coffeeresults'] = models.Cafe.objects.filter(name=d['key']).values()
    except:
        pass
    #...

    # coffeebeansresults results
    # ...

    return render(request, "search.html", d)

def addcafe(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)
    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)

    if request.method == 'POST':
        d['cafe_name'] = request.POST.get('name', '')
        c = models.Cafe(name=d['cafe_name'], owner=d['pk'])
        c.save()
    else:
        d['message'] = 'Unexpected link.'
    return render(request, "profile.html", d)

def profile(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)
    d['key'] = request.GET.get('key', '')
    d['searchbar'] = getSearchBar(d)
    # change to requested user profile number
    d['user_id'] = User.objects.first()

    if request.method == 'POST':
        return addcafe(request)

    return render(request, "profile.html", d)

def users(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    if request.method == 'POST':
        pk = request.POST.get('pk')
        User.objects.get(pk=pk).delete()
        models.Drinker.objects.get(key=pk).delete()
        return HttpResponseRedirect('')

    d['users_list'] = User.objects.all()
    return render(request, "users.html", d)


