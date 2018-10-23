from django.db import models
from django.contrib.auth.models import User

# null? default?

class CoffeePreparation(models.Model):
    """ Preparation of coffee. """
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CoffeeBean(models.Model):
    """ Coffee bean type. """
    name = models.CharField(max_length=64)
    origin = models.CharField(max_length=64, blank=True)
    aroma = models.CharField(max_length=64, blank=True)
    acidity = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        return self.name

class Coffee(models.Model):
    """ Coffee served in some cafe. """
    name = models.CharField(max_length=64)
    place_of_origin = models.CharField(max_length=64, blank=True)
    quality = models.CharField(max_length=64, blank=True)
    taste_description = models.TextField(blank=True)
    # my suggestion - dont change unless you are 100% sure:
    preparation = models.ForeignKey(CoffeePreparation, blank=True, null=True, on_delete=models.SET_NULL)
    #preparation = CoffeePreparation()   # co to je, neda se to resit cizim klicem?
    beans = models.ManyToManyField(CoffeeBean, through="CoffeeContainsBeans")

    def __str__(self):
        return self.name

class CoffeeContainsBeans(models.Model):
    """ Coffee contains certain percentage of different beans. """
    coffee = models.ForeignKey(Coffee, on_delete=models.CASCADE)
    coffeeBean = models.ForeignKey(CoffeeBean, on_delete=models.CASCADE)
    percentage = models.PositiveIntegerField()

"""
class User(models.Model):

    nick = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    surname = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    fav_coffee = models.ManyToManyField(Coffee)
    fav_preparation = models.ManyToManyField(CoffeePreparation)
"""

class Cafe(models.Model):
    """ Cafe. """
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64, blank=True, null=True)
    housenumber = models.PositiveIntegerField(blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    psc = models.PositiveIntegerField(blank=True, null=True)
    opensAt = models.TimeField(blank=True, null=True)
    closesAt = models.TimeField(blank=True, null=True)
    capacity = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.PositiveIntegerField(default='0')
    offers_coffee = models.ManyToManyField(Coffee)
    #employees = models.ManyToManyField(User)       - vubec bych to neresil, nemusime vypisovat vsechny zamestnance kavaren

    def __str__(self):
        return self.name

class Drinker(models.Model):
    """ User of the system. """
    key = models.PositiveIntegerField(default='0')
    fav_coffee = models.ManyToManyField(Coffee)
    fav_preparation = models.ManyToManyField(CoffeePreparation)
    likes_cafe = models.ManyToManyField(Cafe)

class Event(models.Model):
    """ Event. """
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    capacity = models.IntegerField()
    participants = models.ManyToManyField(Drinker)
    coffee_list = models.ManyToManyField(Coffee)
    place = models.ForeignKey(Cafe, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    """ Evaluation. """
    drinker = models.ForeignKey(Drinker, on_delete=models.CASCADE, null=True)
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.drinker + str(value)

class Reaction(models.Model):
    """ Comment. """
    cafe = models.ForeignKey(Cafe, blank=True, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(Drinker, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)     # remove blank!!
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.author





