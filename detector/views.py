from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from .models import Team
from .clean_data import clean_text
# Create your views here.
import openai
import spacy
import time
from .fetch_data import fetch_data
from .response import generate_answer
from .fetch_urldata import fetch_url_data
import requests

openai.api_key = 'Your OpenAI API Key'

def detector(request):
    if request.method == 'GET':
        return render(request,"home.html")

    if request.method == 'POST':

        ques = request.POST['fakenews']

        response = openai.Completion.create(model="text-davinci-003",prompt=ques.capitalize() + "?Is this news information content real or fake?Option: Real or Fake?Give supportive evidence from reliable sources of above?", temperature=1, max_tokens=1000)
        formatted_response = response['choices'][0]['text']
        context = {
            'formatted_response': clean_text(formatted_response),
            'prompt': ques,
        }

        return render(request,"home.html",context)
    
def current_affair(request):
    if request.method == 'GET':
        return render(request,"current.html")

    if request.method == 'POST':

        ques = request.POST['fakenews']

        # Load the pre-trained model
        nlp = spacy.load('en_core_web_sm')
        entities = []
        # Process the sentence using the loaded model
        doc = nlp(ques)

        # Iterate over the entities in the sentence
        for ent in doc.ents:
            # Print the entity text and its label
            entities.append(ent.text)

        articles = fetch_data(ques)
        if len(articles) == 0:
            if len(entities) != 0:
                articles = fetch_data(entities[0])
        formatted_response = generate_answer(ques,articles)

        sources = []
        for article in articles:
            sources.append({
                "url": article["url"],
                "headline": article["headline"],
                "date": article["date"],
                "publisher": article["publisher"]
            })

        context = {
            'formatted_response': clean_text(formatted_response),
            'prompt': ques,
            'sources': sources,
        }

        return render(request,"current.html",context)

def info(request):
    teams = Team.objects.all()
    context = {
        "teams": teams
    }
    return render(request,"info.html",context)

def grover(request):
    if request.method == 'GET':
        return render(request,"url.html")
    
    if request.method == 'POST':

        url = request.POST['news_url']

        data = fetch_url_data(url)
        articles = fetch_data(data)
        formatted_response = generate_answer(data,articles)

        context = {
            'formatted_response': formatted_response,
            'prompt': url,
        }
    return render(request,"url.html",context)

def neutralizer(request):
    if request.method == 'GET':
        return render(request,"neutralizer.html")
    
    if request.method == 'POST':
        query = request.POST['fakenews']

        api_key_checker = '0e5cfd92df8f7fe5e6b7603cad918522'
        url = f"https://api.social-searcher.com/v2/search?q={query}&network=facebook&key={api_key_checker}"
        response = requests.get(url)

        if response.ok:
            data = response.json()
            posts = data["posts"]
        
        context = {
            "posts": posts,
            "prompt": query,
        }

        return render(request,"neutralizer.html",context)

def facebook(request):
    access_token='EAAPQOmGQ7gMBACRb4jYc1Vx57HFAN7ZAR3l2jRrP018i2TYkwJk71Y10B4wGbqmZCInxG8KwyXL706jXiif0oiV1Oso1XoVcVE23TKkJ3wsVY7nDKDJxGTFnEw7zqSHSG5OjBqEa3TABW6MItmW6JGtimWhjOtZAqgLh3iUAs0PXp0qU4vna0cZCE44PQOpApAwf5CXuOAZDZD'
    post_id = ''

    url = 'https://graph.facebook.com/v12.0/{}/report'.format(post_id)

    params = {
        'access_token': access_token,
        'message': 'This post violates Facebook\'s community standards.'
    }

    response = requests.post(url, data=params)

    if response.status_code == 200:
        print('Post reported successfully')
    else:
        print('Error reporting post:', response.json()['error']['message'])

        

