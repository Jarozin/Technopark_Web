from django.shortcuts import render
from . import models
from django.http import HttpResponseNotFound
# Create your views here.


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)


def question(request, question_id):
    if (question_id > len(models.QUESTIONS)):
        return HttpResponseNotFound("Error 404")
    context = {'question': models.QUESTIONS[question_id], 'answers': models.ANSWERS, 'answer_amounts': len(models.ANSWERS)}
    return render(request, 'question.html', context)
