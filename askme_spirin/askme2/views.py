from django.shortcuts import render
from . import models
from django.http import HttpResponseNotFound
# Create your views here.


def index(request):
    context = {'questions': models.QUESTIONS, 'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'index.html', context)


def login(request):
    context = {'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'login.html', context)


def ask(request):
    context = {'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'ask.html', context)


def signup(request):
    context = {'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'signup.html', context)


def settings(request):
    context = {'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'settings.html', context)


def question(request, question_id):
    if (question_id > len(models.QUESTIONS)):
        return HttpResponseNotFound("Error 404")
    context = {'question': models.QUESTIONS[question_id],
               'answers': models.ANSWERS, 'answer_amounts': len(models.ANSWERS),
               'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'question.html', context)

def tag(request, tag_name):
    for tag in models.TAGS:
        if tag['name'] == tag_name:
            context = {'tag': tag, 'questions': models.QUESTIONS, 'members': models.MEMBERS, 'tags': models.TAGS}
            return render(request, 'tag.html', context)
    return HttpResponseNotFound("Error 404")
    
