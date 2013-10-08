from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import generic
from nb_webapp.models import *
#import oauth2 as oauth

def flowingInfo(request):
    loginID = 2           #    according to login

    CardsDict = {}#all information
    FollowingIDList = []
    FollowingDict = {}
    CardsList = []#Cards Information

    flowingList = FollowingInfo.objects.filter(basic_info_id=loginID)
    for nFlowing in flowingList:
        nID = nFlowing.following_info_id
        FollowingIDList.append(nID)
        cards = KnowledgeCard.objects.filter(basic_info_id=nID)
        CardsList = []
        for card in cards:
            CardsList.append(card)

        CardsDict[nID] = CardsList#CardsInformation
        FollowingDict[nID] = BasicInfo.objects.get(user_id=nID)#folowingIntomation

    return render(request, 'Temp/informationFormFriends.html',
                  {'CardsDict': CardsDict,'FollowingDict': FollowingDict,
                   'FollowingIDList': FollowingIDList})

class IndexView(generic.ListView):
    template_name = 'nb_webapp/index.html'

    def get_queryset(self):
        """Return the last five published polls."""
        return "asdf"


# Save member id into db and connect with a internal id.
def register(request):
    error = False
    if 'linkedin-id' in request.GET:
        this_linkedin_id = request.GET['linkedin-id']
        this_name = request.GET['name']
        if not this_linkedin_id:
            error = True
        else:
            getLinkedinData(this_linkedin_id)
            return render(request, 'nb_webapp/register.html',
                          {'LINKEDIN_ID': this_linkedin_id, 'name': this_name})
    return render(request, 'nb_webapp/register.html', {'error': error})


def getLinkedinData(linkedin_id):
    consumer_key = 'gxls9vtr7moe'
    consumer_secret = 'efjIUM6aj3Fza2Nh'
    user_token = '33713a5e-5c84-48b4-a19d-56f9333d5e99'
    user_secret = '2f6c10e6-2413-4fb6-adb4-47c728fbcb2f'

    # Use your API key and secret to instantiate consumer object
    consumer = oauth.Consumer(consumer_key, consumer_secret)

    # Use your developer token and secret to instantiate access token object
    access_token = oauth.Token(
        key=user_token,
        secret=user_secret)
    client = oauth.Client(consumer, access_token)

    # Make call to LinkedIn to retrieve your own profile
    resp, content = client.request(
        "http://api.linkedin.com/v1/people/id=" + linkedin_id + ":(first-name,last-name,id,email-address,phone-numbers,industry)",
        "GET", "")
    basicInfo = BasicInfo(linkedin_member_id=linkedin_id)
    basicInfo.save()
    print content

def loginsignup(request):
    return render(request, 'Temp/loginsignup.html')

def login(request):
    return True

def signup(request):
    post_account_email = request.POST['account_email']
    post_password = request.POST['password']
    # Check for existence
    if BasicInfo.objects.filter(account_email = post_account_email).exists():
        message = "User already exists!"
    else:
        q = BasicInfo(account_email = post_account_email, password = post_password)
        q.save()
        message = "Sign up successfully!"
    return HttpResponse(message)
