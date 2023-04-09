from django.db import models


ANSWERS = [
    {
        'id': i,
        'text': f'Text {i}',
        'correct answer': 0,
        'likes': i + 5,
    }for i in range(30)
]

MEMBERS = [
    {
        'name': f'Name_{i}',
    }for i in range(9)
]
QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'Text {i}',
        'likes': i + 5,
        'tags': [f'Tag_{i}', f'Tag_{i+1}'],
    } for i in range(30)
]


class Like(models.Model):
    state = models.BooleanField()
    user = models.ForeignKey('User', on_delete=models.SET_DEFAULT)


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey('User', on_delete=models.SET_DEFAULT)
    like = models.ForeignKey('Like', on_delete=models.PROTECT)
    tag = models.ManyToManyField('Tag')


class User(models.Model):
    name = models.CharField(max_length=255)


class Answer(models.Model):
    content = models.TextField()
    correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.SET_DEFAULT)
    like = models.ForeignKey('Like', on_delete=models.PROTECT)
