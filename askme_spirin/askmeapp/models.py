from django.db import models
from django.contrib.auth.models import User

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
    user = models.ForeignKey('AskmeUser', on_delete=models.CASCADE)
    def __str__(self):
        return self.state

class Tag(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey('AskmeUser', on_delete=models.CASCADE)
    like = models.ForeignKey('Like', on_delete=models.PROTECT)
    tag = models.ManyToManyField('Tag')
    def __str__(self):
        return self.title

class AskmeUser(models.Model):
    profile = models.OneToOneField(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.profile.get_username()

class Answer(models.Model):
    content = models.TextField()
    correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    user = models.ForeignKey('AskmeUser', on_delete=models.CASCADE)
    like = models.ForeignKey('Like', on_delete=models.PROTECT)
    def __str__(self):
        return self.content
