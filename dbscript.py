# python3 manage.py shell <dbscript.py
# this is a script for filling up a database

# jelikoz jakakoliv zmena v databazi vyzaduje kompletni reset, sem budu psat vkladaci prikazy pro naplneni
# vsechny zaznamy v databazi se mazou nasledovne: python3 manage.py flush

from kavarna import models

test = models.CoffeeBean(name = "zrnko", origin = "cze", aroma = "nevonne", acidity = 10)
test.save()
test2 = models.CoffeeBean(name = "africka namka", origin = "cze", aroma = "nevonne", acidity = 10)
test2.save()
test3 = models.CoffeeBean(name = "moje kavicka", origin = "cze", aroma = "nevonne", acidity = 10)
test3.save()

preparation1 = models.CoffeePreparation(name = "zasterchat")
preparation1.save()

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

testOwner = models.Owner(name = "Jan", surname = "Honzik")
testOwner.save()

testC = models.Cafe(name = "U Martina", street = "Martinovo namesti", housenumber = 47, city = "Brno", psc = 66600,
                opensAt = "9:00", closesAt = "18:00", capacity = 50, description = "Very nice...", owner = models.Owner.objects.first(),
                )
testC.save()





#models.CoffeeBean.objects.all().delete()
#testOwner.delete()
#testC.delete()

exit(0)
