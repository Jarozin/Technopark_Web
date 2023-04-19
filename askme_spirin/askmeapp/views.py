
from django.shortcuts import redirect, render
from django.contrib import auth
from django.urls import reverse

from askmeapp.forms import LoginForm
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
    all_questions = models.Question.objects.get_new()
    questions = paginate(all_questions, request, 3)
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]

    context = {'items': questions,
               'tags': tags, 'members': users}
    return render(request, 'index.html', context)


def hot(request):
    hot_questions = models.Question.objects.get_hot()
    questions = paginate(hot_questions, request, 3)
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]

    context = {'items': questions,
               'tags': tags, 'members': users}
    return render(request, 'hot.html', context)


def login(request):
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    context = {'tags': tags, 'members': users}
    print(request.POST)
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = auth.authenticate(request=request, **login_form.cleaned_data)
        if (user):
            auth.login(request, user)
            return redirect(reverse('index'))
    return render(request, 'login.html', context)


def ask(request):
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    context = {'tags': tags, 'members': users}
    return render(request, 'ask.html', context)


def signup(request):
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    context = {'tags': tags, 'members': users}
    return render(request, 'signup.html', context)


def settings(request):
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    context = {'tags': tags, 'members': users}
    return render(request, 'settings.html', context)


def question(request, question_id):
    try:
        question = models.Question.objects.get_by_id(question_id)
    except:
        return HttpResponseNotFound("Question doesnt exist")
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    question_answers = models.Answer.objects.get_question_answers(question)
    answers = paginate(question_answers, request, 3)
    context = {'main_question': question,
               'items': answers,
               'tags': tags, 'members': users}
    return render(request, 'question.html', context)


def tag(request, tag_name):
    tagged_questions = models.Question.objects.get_by_tag(tag_name)
    if (len(tagged_questions) == 0):
        return HttpResponseNotFound("No questions match the tag")
    questions = paginate(tagged_questions, request, 3)
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    context = {'tag': tag_name, 'items': questions,
               'members': users, 'tags': tags}
    return render(request, 'tag.html', context)
