from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
   text = "<h1>Hello, World!</h1>"
   return HttpResponse(text)

def index(request):
   return render(request, "index.html", {})

def register(request):
    return render(request, "register.html", {})

def signin(request):
    return render(request, "signin.html", {})

# add function with the name matching from urls.py
# def function(request, parameters...):
#       return render(request, file from template, dict())
# watch documentation for more information