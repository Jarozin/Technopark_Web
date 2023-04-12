from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Value, Sum, F
from django.db.models.functions import Coalesce

class Like(models.Model):
    #TODO: сумму лайков можно как доп колонку в таблицу к вопросам/ответам забросить, сами лайки можно разделить на лайки для вопросов и ответов
    common_content = models.ForeignKey(
        'CommonContent', on_delete=models.PROTECT)
    state = models.BooleanField()
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)

    class Meta:
        unique_together=['common_content','user']

    def __str__(self):
        if (self.state):
            like_state = '+1'
        else:
            like_state = '-1'
        return str(self.user) + ': ' + like_state



class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CommonContent(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class QuestionManager(models.Manager):
    def get_new(self):
        return Question.objects.order_by('-creation_date').annotate(likes=Coalesce(Sum(Case(When(common_content__like__state=True, then=Value(
            1)), When(common_content__like__state=False, then=Value(-1)))), 0))

    def get_hot(self):
        return Question.objects.annotate(likes=Coalesce(Sum(Case(When(common_content__like__state=True, then=Value(
            1)), When(common_content__like__state=False, then=Value(-1)))), 0)).order_by('-likes', '-creation_date')

    def get_by_tag(self, tag_name):
        return Question.objects.order_by(
            '-creation_date').filter(tags__name__iexact=tag_name).annotate(likes=Coalesce(Sum(Case(When(common_content__like__state=True, then=Value(
            1)), When(common_content__like__state=False, then=Value(-1)))), 0))

    def get_by_id(self, question_id):
        return Question.objects.annotate(likes=Coalesce(Sum(Case(When(common_content__like__state=True, then=Value(
            1)), When(common_content__like__state=False, then=Value(-1)))), 0)).get(id=question_id)


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    common_content = models.OneToOneField(
        'CommonContent', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.user.get_username()


class AnswerManager(models.Manager):
    def get_question_answers_count(self, question):
        return question.answer_set.all().count()

    def get_question_answers(self, question):
        return question.answer_set.annotate(likes=Coalesce(Sum(Case(When(common_content__like__state=True, then=Value(
            1)), When(common_content__like__state=False, then=Value(-1)))), 0)).order_by('-correct', '-likes', '-creation_date')


class Answer(models.Model):
    content = models.TextField()
    correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    common_content = models.OneToOneField(
        'CommonContent', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = AnswerManager()

    def __str__(self):
        return self.content[:40]
