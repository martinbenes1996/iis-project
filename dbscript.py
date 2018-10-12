# python3 manage.py shell <dbscript.py
# this is a script for filling up a database

# jelikoz jakakoliv zmena v databazi vyzaduje kompletni reset, sem budu psat vkladaci prikazy pro naplneni
# vsechny zaznamy v databazi se mazou nasledovne: python3 manage.py flush

from kavarna import models

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



#models.CoffeeBean.objects.all().delete()
#testOwner.delete()
#testC.delete()

exit(0)
