from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import openai

openai.api_key = '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'

def detector(request):
    if request.method == 'GET':
        return render(request,"home.html")

    if request.method == 'POST':

        ques = request.POST['fakenews']

        response = openai.Completion.create(model="text-davinci-003",prompt=ques + "?Is this news content real or fake?", temperature=1, max_tokens=1000)
        formatted_response = response['choices'][0]['text']

        context = {
            'formatted_response': formatted_response,
            'prompt': ques,
        }

        return render(request,"home.html",context)

def info(request):
    return render(request,"info.html")

def grover(request):
    if request.method == 'GET':
        return render(request,"url.html")
    
    if request.method == 'POST':

        ques = request.POST['news_url']

        response = openai.Completion.create(model="text-davinci-003",prompt=ques + ".Read the news from the link.Is this news Real or Fake?options: Real or Fake", temperature=1, max_tokens=1000)
        formatted_response = response['choices'][0]['text']

        context = {
            'formatted_response': formatted_response,
            'prompt': ques,
        }
    return render(request,"url.html",context)
