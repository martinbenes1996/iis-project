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
    
    if request.method == 'GET':
        subject = request.GET['pk_subject']
        reactingto = request.GET['reactingto']
        score = int(request.GET['score'])
        text = request.GET.get('text', '')

        if reactingto == 'Cafe':
            s = models.Cafe.objects.get(id=subject)
            f = models.Reaction.objects.filter(author=d['loggeduser'],cafe=s).exclude(score=None)
            if f.count() > 0:
                f.delete()
            r = models.Reaction(cafe=s, author=d['loggeduser'], score=score, text=text)
            countScore = getCafeScore
        elif reactingto == 'Reaction':
            s = models.Reaction.objects.get(id=subject)
            f = models.Reaction.objects.filter(author=d['loggeduser'],react=s).exclude(score=None)
            if f.count() > 0:
                f.delete()
            r = models.Reaction(react=s, author=d['loggeduser'], score=score, text=text)
            countScore = getReactionScore
        elif reactingto == 'Event':
            s = models.Event.objects.get(id=subject)
            f = models.Reaction.objects.filter(author=d['loggeduser'],event=s).exclude(score=None)
            if f.count() > 0:
                f.delete()
            r = models.Reaction(event=s, author=d['loggeduser'], score=score, text=text)
            countScore = getEventScore
        else:
            raise Exception('Unknown Reaction Subject.')
        
        r.save()
        return countScore(s)

    else:
        raise Exception('POST request')

def processCafeLike(request):
    d = generateDict(request)
    if 'message' in d:
        return errLogout(request, d)
    
    if request.method == 'GET':
        pk_cafe = request.GET['pk']
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
    

    