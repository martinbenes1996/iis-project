# python3 manage.py shell <dbscript.py
# this is a script for filling up a database

# jelikoz jakakoliv zmena v databazi vyzaduje kompletni reset, sem budu psat vkladaci prikazy pro naplneni
# vsechny zaznamy v databazi se mazou nasledovne: python3 manage.py flush

from kavarna import models

# coffeePreparation
preparation1 = models.CoffeePreparation(name = "zasterchat")
preparation1.save()
preparation2 = models.CoffeePreparation(name = "uvarit pri mesicku", description = "za temne noci se vypravte" +
    " do hlubokeho lesa, natrhejte kapradi, zapalte a v hustem kouri varte kafe. Predneste zaklinadlo.")
preparation2.save()

# coffeeBean
test = models.CoffeeBean(name = "zrnko", origin = "cze", aroma = "nevonne", acidity = 10)
test.save()
test2 = models.CoffeeBean(name = "africka namka", origin = "cze", aroma = "nevonne", acidity = 10)
test2.save()
test3 = models.CoffeeBean(name = "moje kavicka", origin = "cze", aroma = "nevonne", acidity = 10)
test3.save()

# coffee + bean percentage input

coffee1 = models.Coffee(name = "Ondrovo prekvapeni", preparation = models.CoffeePreparation.objects.first())
coffee1.save()
#coffee1 = models.Coffee(name = "Ondrovo prekvapeni", preparation = models.CoffeePreparation.objects.get(name = "zasterchat"))
coffee2 = models.Coffee(name = "Pivni kava")
coffee2.save()

coffeecontainsbeans = models.CoffeeContainsBeans(coffee = coffee1, coffeeBean = models.CoffeeBean.objects.first(),
                                                percentage = 100)
coffeecontainsbeans.save()
coffeecontainsbeans2 = models.CoffeeContainsBeans(coffee = coffee2, coffeeBean = models.CoffeeBean.objects.first(),
                                                percentage = 100)
coffeecontainsbeans2.save()


# owner
testOwner = models.Owner(name = "Jan", surname = "Honzik")
testOwner.save()

# cafe
testC = models.Cafe(name = "U Martina", street = "Martinovo namesti", housenumber = 47, city = "Brno", psc = 66600,
                opensAt = "9:00", closesAt = "18:00", capacity = 50, description = "Very nice...", owner = models.Owner.objects.first(),
                )
testC.save()

# user
testUser1 = models.User(nick = "darkDemon666", name = "Frantisek", email = "franta@mymail.com",
                        surname = "Velmichytry", password = "12345")
testUser1.save()
testUser1.fav_coffee.add(models.Coffee.objects.first())
testUser1.fav_preparation.add(models.CoffeePreparation.objects.first(), models.CoffeePreparation.objects.last())
testUser1.likes_cafe.add(models.Cafe.objects.first())
# pom.fav_preparation.all() -> zobrazeni vsech polozek ManyToManyField

# event
testEvent1 = models.Event(name = "labuznicke setkani", price = 100, capacity = 20, place = models.Cafe.objects.first())
testEvent1.save()
testEvent1.participants.add(models.User.objects.first())
testEvent1.coffee_list.add(models.Coffee.objects.first())

# evaluation
testEvaluation1 = models.Evaluation(user = models.User.objects.first(), value = 8)
testEvaluation1.save()

# reaction
testReaction1 = models.Reaction(cafe = models.Cafe.objects.first(), author = models.User.objects.first(),
                                text = "dobry kafe!", evaluation = models.Evaluation.objects.first())
testReaction1.save()




#models.CoffeeBean.objects.all().delete()
#testOwner.delete()
#testC.delete()

exit(0)
