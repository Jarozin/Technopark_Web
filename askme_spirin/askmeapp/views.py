from django.shortcuts import render
from . import models
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
# Create your views here.


def paginate(object_list, request, per_page=3):
    if (per_page < 0):
        per_page = 3
    p = Paginator(object_list, per_page)
    page = request.GET.get('page')
    object = p.get_page(page)
    return object


def index(request):
    all_questions = models.Question.objects.all()
    question_tags = models.Tag.objects.get_questions_tags(all_questions)
    all_questions = list(zip(all_questions, question_tags))
    questions = paginate(all_questions, request, 3)
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]

    context = {'items': questions,
               'tags': tags, 'members': users}
    return render(request, 'index.html', context)


def hot(request):
    questions = paginate(models.QUESTIONS, request, 3)
    tags = set()
    for question in models.QUESTIONS:
        for tag in question['tags']:
            tags.add(tag)
    context = {'items': questions,
               'tags': tags, 'members': models.MEMBERS}
    return render(request, 'hot.html', context)


def login(request):
    tags = set()
    for question in models.QUESTIONS:
        for tag in question['tags']:
            tags.add(tag)
    context = {'tags': tags, 'members': models.MEMBERS}
    return render(request, 'login.html', context)


def ask(request):
    tags = set()
    for question in models.QUESTIONS:
        for tag in question['tags']:
            tags.add(tag)
    context = {'tags': tags, 'members': models.MEMBERS}
    return render(request, 'ask.html', context)


def signup(request):
    tags = set()
    for question in models.QUESTIONS:
        for tag in question['tags']:
            tags.add(tag)
    context = {'tags': tags, 'members': models.MEMBERS}
    return render(request, 'signup.html', context)


def settings(request):
    tags = set()
    for question in models.QUESTIONS:
        for tag in question['tags']:
            tags.add(tag)
    context = {'tags': tags, 'members': models.MEMBERS}
    return render(request, 'settings.html', context)


def question(request, question_id):
    if (question_id > len(models.QUESTIONS)):
        return HttpResponseNotFound("Error 404")
    tags = set()
    for question in models.QUESTIONS:
        for tag in question['tags']:
            tags.add(tag)
    answers = paginate(models.ANSWERS, request, 3)
    context = {'question': models.QUESTIONS[question_id],
               'items': answers, 'answer_amounts': len(models.ANSWERS),
               'tags': tags, 'members': models.MEMBERS}
    return render(request, 'question.html', context)


def tag(request, tag_name):
    tags = set()
    for question in models.QUESTIONS:
        for tag in question['tags']:
            tags.add(tag)
    for tag in tags:
        if tag == tag_name:
            tagged_questions = list()
            for question in models.QUESTIONS:
                for tag in question['tags']:
                    if tag == tag_name:
                        tagged_questions.append(question)
                        break
            questions = paginate(tagged_questions, request, 3)
            context = {'tag': tag_name, 'items': questions,
                       'members': models.MEMBERS, 'tags': tags}
            return render(request, 'tag.html', context)
    return HttpResponseNotFound("Error 404")
