from kavarna import models
from django.contrib.auth.models import User
from statistics import mean 

def generateDict(request):
    try:
        email = request.COOKIES['user']
        if User.objects.get(email=email) != None:
            d = {'loggeduser'    : User.objects.get(email=email),
                 'loggeddrinker' : models.Drinker.getData(email) }
        else:
            d = {'message'   : 'Unknown user'}
    except:
        d = {}
    d['key'] = request.GET.get('key', '')

    return d

def getScore(l):
    if len(l) == 0: return 0
    return mean(l)
def getCafeScore(c):
    return getScore( [r.score for r in models.Reaction.objects.all().filter(cafe=c)] )
def getEventScore(e):
    return getScore( [r.score for r in models.Reaction.objects.all().filter(event=e)] )
def getReactionScore(rr):
    return getScore( [r.score for r in models.Reaction.objects.all().filter(reaction=rr)] )

def processScore(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)
    
    if request.method == 'POST':
        subject = request.POST['pk_subject']
        reactingto = request.POST['reactingto']
        score = int(request.POST['score'])
        text = request.POST.get('text', '')
        print("adding reaction by ", d['loggeduser'], " to ", subject, ": ", score)

        if reactingto == 'Cafe':
            s = models.Cafe.objects.get(id=subject)
            r = models.Reaction(cafe=s, author=d['loggeduser'], score=score, text=text)
        elif reactingto == 'Reaction':
            s = models.Reaction.objects.get(id=subject)
            r = models.Reaction(react=s, author=d['loggeduser'], score=score, text=text)
        elif reactingto == 'Event':
            s = models.Event.objects.get(id=subject)
            r = models.Reaction(event=s, author=d['loggeduser'], score=score, text=text)
        else:
            raise Exception('Unknown Reaction Subject.')
        
        r.save()

    else:
        raise Exception('GET request')

def processCafeLike(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)
    
    if request.method == 'POST':
        pk_cafe = request.POST['pk']
        d['cafe'] = models.Cafe.objects.get(pk=pk_cafe)
        if d['cafe'] in d['loggeddrinker'].likes_cafe.all():
            d['loggeddrinker'].likes_cafe.remove(d['cafe'])
            return False
        else:
            d['loggeddrinker'].likes_cafe.add(d['cafe'])
            return True

def processEventParticipate(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)
    
    if request.method == 'POST':
        pk_event = request.POST['pk']
        d['event'] = models.Event.objects.get(pk=pk_event)
        if d['loggeduser'] in d['event'].participants.all():
            d['event'].participants.remove(d['loggeduser'])
            return False
        else:
            d['event'].participants.add(d['loggeduser'])
            return True
    

    