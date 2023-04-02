from django.shortcuts import render
from . import models
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    p = Paginator(models.QUESTIONS, 3)
    page = request.GET.get('page')
    questions = p.get_page(page)
    context = {'items': questions,
               'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'index.html', context)


def hot(request):
    p = Paginator(models.QUESTIONS, 3)
    page = request.GET.get('page')
    questions = p.get_page(page)
    context = {'items': questions,
               'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'hot.html', context)


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
    p = Paginator(models.ANSWERS, 3)
    page = request.GET.get('page')
    answers = p.get_page(page)
    context = {'question': models.QUESTIONS[question_id],
               'items': answers, 'answer_amounts': len(models.ANSWERS),
               'tags': models.TAGS, 'members': models.MEMBERS}
    return render(request, 'question.html', context)


def tag(request, tag_name):
    for tag in models.TAGS:
        if tag['name'] == tag_name:
            p = Paginator(models.QUESTIONS, 3)
            page = request.GET.get('page')
            questions = p.get_page(page)
            context = {'tag': tag, 'items': questions,
                       'members': models.MEMBERS, 'tags': models.TAGS}
            return render(request, 'tag.html', context)
    return HttpResponseNotFound("Error 404")
