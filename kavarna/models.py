from django.db import models

# null? default?

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

    #def __str__(self):
    #   return self.name

class Coffee(models.Model):
    """ Coffee served in some cafe. """
    name = models.CharField(max_length=64)
    place_of_origin = models.CharField(max_length=64, blank=True)
    quality = models.CharField(max_length=64, blank=True)
    taste_description = models.TextField(blank=True)
    preparation = CoffeePreparation()   # co to je, neda se to resit cizim klicem?
    beans = models.ManyToManyField(CoffeeBean, blank=True)  # !!! pridat atribut kava_obs_zrna
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
    # je moznost oddelit tabulku uzivatel a zamestnanec. Zamestnanec se vztahuje k dane kavarne, ne k nasemu systemu.
    # My delame system mapujici kavarny a ne is jednotlivych kavaren -> nepotrebujeme vubec znat zamestnance
    # jednotlivych kavaren a zamestnavatel neni automaticky uzivatel registrovany v nasem is. Toto je muj navrh:

class Owner(models.Model):
    """ Owner of a cafe. """
    name = models.CharField(max_length=64)
    email = models.EmailField(blank=True)
    surname = models.CharField(max_length=64)
    # picture = models.         # fotka majitele

class Cafe(models.Model):
    """ Cafe. """
    name = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    housenumber = models.PositiveIntegerField(blank=True)
    city = models.CharField(max_length=64)
    psc = models.PositiveIntegerField(blank=True)
    opensAt = models.TimeField()
    closesAt = models.TimeField()
    capacity = models.PositiveSmallIntegerField(blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    offers_coffee = models.ManyToManyField(Coffee)
    #employees = models.ManyToManyField(User)       - vubec bych to neresil, nemusime vypisovat vsechny zamestnance kavaren

class User(models.Model):
    """ User of the system. """
    nick = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    email = models.EmailField()
    surname = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    fav_coffee = models.ManyToManyField(Coffee)
    fav_preparation = models.ManyToManyField(CoffeePreparation)
    likes_cafe = models.ManyToManyField(Cafe)

class Event(models.Model):
    """ Event. """
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    capacity = models.IntegerField()
    participants = models.ManyToManyField(User)
    Coffee_list = models.ManyToManyField(Coffee)
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





