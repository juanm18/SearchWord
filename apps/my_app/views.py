from django.shortcuts import render, HttpResponse,redirect
import requests
try: import simplejson as json
except ImportError: import json
from django.contrib import messages
from models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt, csrf_protect

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'my_app/main.html')

def word(request):
    json = ''
    resp = ''
    pronunciation = ''
    types = ''
    examples = ''
    errors=[]
    if len(request.POST['search_word'])==0:
        errors.append("Enter a Word you'd like")
        return redirect('/', {'errors':errors})
    else:
        search_word = request.POST['search_word']
        app_id = 'f6753694'
        app_key = 'e76b8f1b1eb4e0e9bff4e2a56bef21e8'
        language = 'en'

        # complete url for API request
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + search_word.lower()
        #custom headers neccessary for request
        headers = {"app_id":app_id, "app_key":app_key}

        #making request to url including headers
        raw = requests.get(url, headers=headers)
        if raw.status_code == 404:
            errors.append('Word Not Found, try another!')
        else:
            json = raw.json()
            resp = json['results']
            pronunciation = resp[0]['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling']
            types = resp[0]['lexicalEntries'][0]['lexicalCategory']
            examples = []
            try:
                examples = resp[0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples']
            except:
                pass

    return render(request, 'my_app/definition.html',{'search_word':search_word, 'raw':raw, 'resp':resp, 'pronunciation':pronunciation, 'types':types, 'examples':examples, 'errors':errors})
