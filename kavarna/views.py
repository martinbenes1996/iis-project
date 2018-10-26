import re

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Context, Template
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.http import Http404

from kavarna import models

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
        if User.objects.get(email=email) != None:
            d = {'loggeduser'    : User.objects.get(email=email),
                 'loggeddrinker' : models.Drinker.getData(email) }
        else:
            d = {'message'   : 'Unknown user'}
    except:
        d = {}
    d['key'] = request.GET.get('key', '')

    return d


def index(request):
    #models.Drinker.objects.all().delete()
    #User.objects.all().delete()
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    print(d.keys())
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
            d['message'] = 'Not matching passwords.'
            return render(request, "register.html", d)
        # invalid email
        #if re.match(r'.+@.+\..+', d['email']) is None:
        #    d['message'] = 'Invalid email.'
        #    return render(request, "register.html", d)
        try:
            user = User.objects.create_user(d['register_email'], password=d['password'])
        except IntegrityError:
            d['message'] = 'Invalid data.'
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
        #    v['message'] = 'Invalid email.'
        #    return render(request, "signin.html", v)

        # go to home
        try:
            u = User.objects.get(username = d['email'])
        except:
            d['message'] = 'No user with given email'
            return render(request, "signin.html", d)

        user = authenticate(username=d['email'], password=d['password'])
        if user is not None:
            response = redirect('')
            response.set_cookie('user', d['email'], max_age=7200)
            return response
        else:
            d['message'] = 'Incorrect password'
            return render(request, "signin.html", d)

    return render(request, "signin.html", d)

def search(request):

    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    # cafe results
    try:
        d['caferesults'] = models.Cafe.objects.filter(name=d['key']).values()
    except:
        pass
    # ...

    # coffee results
    try:
        d['coffeeresults'] = models.Coffee.objects.filter(name=d['key']).values()
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

    if request.method == 'POST':
        if 'loggeduser' not in d:
            d['message'] = 'You must login before creating cafe'
        d['cafe_name'] = request.POST['name']
        d['cafe_street'] = request.POST.get('street')
        d['cafe_housenumber'] = request.POST.get('housenumber')
        d['cafe_city'] = request.POST.get('city')
        d['cafe_psc'] = request.POST.get('psc')
        d['cafe_opensat'] = request.POST.get('opensat')
        d['cafe_closesat'] = request.POST.get('closesat')
        d['cafe_capacity'] = request.POST.get('capacity')
        d['cafe_description'] = request.POST.get('description')
        #for k,v in d.items():
        #    if v == '':
        #        d[k] = None
       # if d['cafe_capacity'] == '': d['cafe_capacity'] = 0

        print(d)
        c = models.Cafe(name=d['cafe_name'],
                        street=d['cafe_street'],
                        housenumber=d['cafe_housenumber'],
                        city=d['cafe_city'],
                        psc=d['cafe_psc'],
                        opensAt=d['cafe_opensat'],
                        closesAt=d['cafe_closesat'],
                        #capacity=d['cafe_capacity'],
                        description=d['cafe_description'],
                        owner=d['loggeduser'])
        c.save()
        return redirect('cafes')
    else:
        d['message'] = 'Unexpected link.'
    return render(request, "addcafe.html", d)

def modifycafe(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    if request.method == 'POST':
        if 'loggeduser' not in d:
            d['message'] = 'You must login before modifying cafe'

        d['cafe_name'] = request.POST['name']
        d['cafe_street'] = request.POST.get('street')
        d['cafe_housenumber'] = request.POST.get('housenumber')
        d['cafe_city'] = request.POST.get('city')
        d['cafe_psc'] = request.POST.get('psc')
        d['cafe_opensat'] = request.POST.get('opensat')
        d['cafe_closesat'] = request.POST.get('closesat')
        d['cafe_capacity'] = request.POST.get('capacity')
        d['cafe_description'] = request.POST.get('description')
        next_url = request.POST.get('next_url')
        cafe = models.Cafe.objects.get(pk=request.POST.get('cafe'))
        #cafe = request.POST.get('cafe')
        #for k,v in d.items():
        #    if v == '':
        #        d[k] = None
        # if d['cafe_capacity'] == '': d['cafe_capacity'] = 0

        print(d)
        cafe.name=d['cafe_name']
        cafe.street=d['cafe_street']
        cafe.housenumber=d['cafe_housenumber']
        cafe.city=d['cafe_city']
        cafe.psc=d['cafe_psc']
        cafe.opensAt=d['cafe_opensat']
        cafe.closesAt=d['cafe_closesat']
        cafe.capacity=d['cafe_capacity']
        cafe.description=d['cafe_description']
        cafe.save()

        return redirect(next_url, permanent=True)
    elif request.method == 'GET':
        cafe_id = request.GET.get('pk')
        d['cafe'] = models.Cafe.objects.get(pk=cafe_id)
        d['next_url'] = request.GET.get('request_path', '/')
    else:
        d['message'] = 'Unexpected link.'

    return render(request, "modifycafe.html", d)


def profile(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    # change to requested user profile number
    if request.method == 'GET':
        user_id = request.GET.get('user', d['loggeduser'].pk)
        d['user_profile'] = User.objects.get(pk=user_id)
    else:
        d['user_profile'] = User.objects.first()

    return render(request, "profile-info.html", d)

def profile_cafe(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    # change to requested user profile number
    if request.method == 'GET':
        user_id = request.GET.get('user', d['loggeduser'].pk) #User.objects.get(email=d['loggeduser']).pk)
        d['user_profile'] = User.objects.get(pk=user_id)
    else:
        d['user_profile'] = User.objects.first()

    #d['user_cafes_list'] = models.Cafe.objects.all()
    d['user_cafes_list'] = models.Cafe.objects.filter(owner=d['user_profile'])#.values()

    return render(request, "profile-cafe.html", d)

def deletecafe(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    if request.method == 'GET':
        next_url = request.GET.get('request_path', '/')
        pk_cafe = request.GET.get('pk')
        models.Cafe.objects.get(pk=pk_cafe).delete()

    return redirect(next_url, permanent=True)

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

def cafes(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    if request.method == 'POST':
        pk = request.POST.get('pk')
        models.Cafe.objects.get(pk=pk).delete()
        return HttpResponseRedirect('')

    d['cafes_list'] = models.Cafe.objects.all()
    d['users_list'] = User.objects.all()
    d['drinkers_list'] = models.Drinker.objects.all()
    return render(request, "cafes.html", d)

def cafe(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    if request.method == 'GET':
        cafeid = request.GET['id']
        print(cafeid)
        d['cafe'] = models.Cafe.getData(cafeid)

        return render(request, "cafe-info.html", d)

def cafe_coffee(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    if request.method == 'GET':
        cafeid = request.GET['id']
        print(cafeid)
        d['cafe'] = models.Cafe.getData(cafeid)
        d['owner'] = d['cafe'].owner    # returns object User

        print(d['cafe'].offers_coffee.all())    # asi
        d['cafe_coffee_list'] = d['cafe'].offers_coffee.all()
        return render(request, "cafe-coffee.html", d)
    #raise Http404("Massive internal error!!")


    #d['user_cafes_list'] = models.Cafe.objects.all()
    #d['cafe_coffee_list'] = models.Coffee.objects.filter(owner=d['user_profile'])#.values()

    #return render(request, "profile-cafe.html", d)

def addcoffee(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    if request.method == 'POST':
        if 'loggeduser' not in d:
            d['message'] = 'You must login before creating cafe'
        d['coffee_name'] = request.POST['name']
        d['coffee_placeoforigin'] = request.POST.get('placeoforigin', None)
        d['coffee_quality'] = request.POST.get('quality', None)
        d['coffee_taste'] = request.POST.get('taste', None)
        d['coffee_preparation'] = request.POST.get('preparation', None)
        d['coffee_bean'] = request.POST.get('bean', None)
        d['coffee_bean_perc'] = request.POST.get('beanperc', None)
        cafeid = request.POST['cafeid']
        d['cafe'] = models.Cafe.getData(cafeid)
        #for k,v in d.items():
        #    if v == '':
        #        d[k] = None
       # if d['cafe_capacity'] == '': d['cafe_capacity'] = 0

        print(d)

        c = models.Coffee()
        c.name=d['coffee_name']
        #if d['coffee_placeoforigin'] != None:
        c.place_of_origin=d['coffee_placeoforigin']
        #if d['coffee_quality'] != None:
        c.quality=d['coffee_quality']
        #if d['coffee_taste'] != None:
        c.taste_description=d['coffee_taste']
        c.preparation=models.CoffeePreparation.objects.get(pk=d['coffee_preparation'])
        c.save()

        d['cafe'].offers_coffee.add(c)  # add coffee to cafe
        contains = models.CoffeeContainsBeans() # add percentage of coffee beans
        contains.coffee = c
        contains.coffeeBean = models.CoffeeBean.objects.get(pk=d['coffee_bean'])
        contains.percentage = d['coffee_bean_perc']
        contains.save()

        return redirect('/profile/')
    elif request.method == 'GET':
        cafeid = request.GET['cafeid']
        d['cafe'] = models.Cafe.getData(cafeid)
        d['preparations'] = models.CoffeePreparation.objects.all()
        d['beans'] = models.CoffeeBean.objects.all()
    else:
        d['message'] = 'Unexpected link.'
    return render(request, "addcoffee.html", d)

def deletecoffee(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)

    if request.method == 'GET':
        next_url = request.GET.get('request_path', '/')
        pk_coffee = request.GET.get('pk')
        models.Coffee.objects.get(pk=pk_coffee).delete()

    return redirect(next_url, permanent=True)
