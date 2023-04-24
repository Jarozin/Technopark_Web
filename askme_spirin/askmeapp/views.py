
from django.shortcuts import redirect, render
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from askmeapp.forms import AnswerForm, LoginForm, ProfileRegistrationForm, QuestionForm, RegistrationForm, SettingsForm
from . import models
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
# Create your views here.


def get_answer_page(object_list, answer, per_page=3):
    if (per_page <= 0):
        per_page = 3
    p = Paginator(object_list, per_page)
    for page in p.page_range:
        object = p.get_page(page)
        print(answer)
        print(object.object_list)
        if answer in object.object_list:
            return page
    return 1


def paginate(object_list, request, per_page=3):
    if (per_page <= 0):
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
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(
                request=request, **login_form.cleaned_data)
            if (user):
                auth.login(request, user)
                url = request.POST.get('next', False)
                if not url:
                    url = reverse('index')
                return redirect(url)
            login_form.add_error(None, "Invalid username/password")
    context = {'tags': tags, 'members': users, 'form': login_form}
    return render(request, 'login.html', context)


@login_required
def ask(request):
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    if request.method == 'GET':
        question_form = QuestionForm()
    elif request.method == 'POST':
        question = models.Question(user=models.Profile.objects.get(user=request.user))
        question_form = QuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question = question_form.save()
            return redirect(reverse('question', kwargs={'question_id':question.id}))
    context = {'tags': tags, 'members': users, 'form': question_form}
    return render(request, 'ask.html', context)


def signup(request):
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    if request.method == 'GET':
        registration_form = RegistrationForm()
        profile_form = ProfileRegistrationForm()
    elif request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST, request.FILES)
        if registration_form.is_valid() and profile_form.is_valid():
            user = registration_form.save()
            profile = models.Profile(user=user, avatar=profile_form.cleaned_data['avatar'])
            profile.save()
            auth.login(request, user)
            return redirect(reverse('index'))
    context = {'tags': tags, 'members': users, 'form': registration_form, 'profile_form': profile_form}
    return render(request, 'signup.html', context)


@login_required
def settings(request):
    if request.method == 'GET':
        try:
            settings_form = SettingsForm(instance=request.user)
            profile = models.Profile.objects.get(user=request.user)
            profile_form = ProfileRegistrationForm(instance=profile)
        except:
            return HttpResponseNotFound('Registration process went wrong')
    elif request.method == 'POST':
        settings_form = SettingsForm(request.POST, instance=request.user)
        profile = models.Profile.objects.get(user=request.user)
        profile_form = ProfileRegistrationForm(request.POST, request.FILES, instance=profile)
        if settings_form.is_valid() and profile_form.is_valid():
            settings_form.save()
            profile_form.save()
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    context = {'tags': tags, 'members': users, 'form': settings_form, 'profile_form': profile_form}
    return render(request, 'settings.html', context)


def question(request, question_id):
    try:
        question = models.Question.objects.get_by_id(question_id)
    except:
        return HttpResponseNotFound("Question doesnt exist")
    tags = models.Tag.objects.all()[:10]
    users = models.User.objects.all()[:10]
    question_answers = models.Answer.objects.get_question_answers(question)
    answers = paginate(question_answers, request)
    if request.method == 'GET':
        answer_form = AnswerForm()
    elif request.method == 'POST':
        #Потребовать авторизацию юзера
        if not request.user.is_authenticated:
            url = reverse('login') + '?next=' + request.get_full_path()
            return redirect(url)
        #Тут может помереть(get)
        profile = models.Profile.objects.get(user=request.user)
        answer = models.Answer(user=profile, question_id=question_id)
        answer_form = AnswerForm(request.POST, instance=answer)
        if answer_form.is_valid():
            answer = answer_form.save()
            page_number = get_answer_page(question_answers, answer)
            url = reverse('question', kwargs={'question_id':question_id}) + '?page=' + str(page_number)
            return redirect(url)
    context = {'main_question': question,
               'items': answers,
               'tags': tags, 'members': users, 'form': answer_form}
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


@login_required
def logout(request):
    auth.logout(request)
    url = request.GET.get('next', False)
    if not url:
        url = reverse('index')
    return redirect(url)
