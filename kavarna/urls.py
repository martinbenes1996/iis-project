"""kavarna URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from kavarna import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name=''),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('search/', views.search, name='search'),
    path('users/', views.users, name='users'),
    path('cafes/', views.cafes, name='cafes'),
    path('profile/', views.profile, name='profile'),
    path('deletecafe/', views.deletecafe, name='deletecafe'),
    path('modifycafe/', views.modifycafe, name='modifycafe'),
    path('addcafe/', views.addcafe, name='addcafe'),
    path('logout/', views.logout, name='logout'),
    path('cafe/', views.cafe, name='cafe'),
    path('cafe/score/', views.cafescore, name='cafescore'),
    path('coffee/', views.coffee, name='coffee'),
    path('event/', views.event, name='event'),
    path('addcoffee/', views.addcoffee, name='addcoffee'),
    path('modifycoffee/', views.modifycoffee, name='modifycoffee'),
    path('deletecoffee/', views.deletecoffee, name='deletecoffee'),
    path('addevent/', views.addevent, name='addevent'),
    path('deleteevent/', views.deleteevent, name='deleteevent'),
    path('participateevent/', views.participateevent, name='participateevent'),
    path('deleteparticipateevent/', views.deleteparticipateevent, name='deleteparticipateevent'),
    path('addcoffeeevent/', views.addcoffeeevent, name='addcoffeeevent'),
    path('deletecoffeeevent/', views.deletecoffeeevent, name='deletecoffeeevent'),
    path('react/', views.react, name='react')
]
