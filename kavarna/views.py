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
