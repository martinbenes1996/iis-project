from django.db import models

class MyModel(models.Model):
    """ Parent for all the models. """
    name = models.CharField(max_length=64)
class MyAddress(models.Model):
    """ Address. """
    street = models.CharField(max_length=64)
    housenumber = models.PositiveIntegerField(blank=True)
    city = models.CharField(max_length=64)
class MySchedule(models.Model):
    """ Schedule. """
    opensAt = models.TimeField()
    closesAt = models.TimeField()


class CoffeePreparation(MyModel):
    """ Preparation of coffee. """
    description = models.TextField(blank=True)

class CoffeeBean(MyModel):
    """ Coffee bean type. """
    origin = models.CharField(max_length=64, blank=True)
    aroma = models.CharField(max_length=64, blank=True)
    acidity = models.PositiveSmallIntegerField(blank=True)

class Coffee(MyModel):
    """ Coffee served in some cafe. """
    preparation = CoffeePreparation()
    beans = models.ManyToManyField(CoffeeBean, blank=True)

class User(MyModel):
    """ User of the system. """
    email = models.EmailField()
    surname = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

class Cafe(MyModel):
    """ Cafe. """
    address = MyAddress()
    schedule = MySchedule()
    capacity = models.PositiveSmallIntegerField(blank=True)
    description = models.TextField(blank=True)
    owner = User()

class Event(MyModel):
    """ Event. """
    price = models.IntegerField()
    capacity = models.IntegerField()
    participants = models.ManyToManyField(User)





    