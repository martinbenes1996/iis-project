from django.db import models

class CoffeePreparation(models.Model):
    """ Preparation of coffee. """
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

class CoffeeBean(models.Model):
    """ Coffee bean type. """
    name = models.CharField(max_length=64)
    origin = models.CharField(max_length=64, blank=True)
    aroma = models.CharField(max_length=64, blank=True)
    acidity = models.PositiveSmallIntegerField(blank=True)

class Coffee(models.Model):
    """ Coffee served in some cafe. """
    name = models.CharField(max_length=64)
    preparation = CoffeePreparation()
    beans = models.ManyToManyField(CoffeeBean, blank=True)  

class User(models.Model):
    """ User of the system. """
    name = models.CharField(max_length=64)
    email = models.EmailField()
    surname = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    preparation = models.ManyToManyField(CoffeePreparation)

class Cafe(models.Model):
    """ Cafe. """
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    housenumber = models.PositiveIntegerField(blank=True)
    city = models.CharField(max_length=64)
    opensAt = models.TimeField()
    closesAt = models.TimeField()
    capacity = models.PositiveSmallIntegerField(blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #employees = models.ManyToManyField(User)

class Event(models.Model):
    """ Event. """
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    capacity = models.IntegerField()
    participants = models.ManyToManyField(User)
    place = models.ForeignKey(Cafe, on_delete=models.CASCADE)

class Evaluation(models.Model):
    """ Evaluation. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField()

class Reaction(models.Model):
    """ Comment. """
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.ForeignKey('self', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    date = models.DateTimeField()
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)





    