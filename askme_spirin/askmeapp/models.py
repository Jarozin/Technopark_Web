from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Value, Sum, F
from django.db.models.functions import Coalesce

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


class LikeManager(models.Manager):
    def get_question_likes_total(self, question):
        likes = question.common_content.like_set.aggregate(sum=Coalesce(
            Sum(Case(When(state=True, then=Value(1)), When(state=False, then=Value(-1)))), 0))
        return likes['sum']

    def get_questions_likes_totals(self, questions):
        likes = list()
        for question in questions:
            count = self.get_question_likes_total(question)
            likes.append(count)
        return likes


class Like(models.Model):
    common_content = models.ForeignKey(
        'CommonContent', on_delete=models.PROTECT)
    state = models.BooleanField()
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    objects = LikeManager()

    def __str__(self):
        if (self.state):
            like_state = '+1'
        else:
            like_state = '-1'
        return str(self.user) + ': ' + like_state


class TagManager(models.Manager):
    def get_questions_tags(self, questions):
        questions_tags = list()
        for question in questions:
            tags = question.tags.all()
            questions_tags.append(tags)
        return questions_tags


class Tag(models.Model):
    name = models.CharField(max_length=255)
    objects = TagManager()

    def __str__(self):
        return self.name


class CommonContent(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class QuestionManager(models.Manager):
    def get_new(self):
        all_questions = Question.objects.order_by('-creation_date')
        question_tags = Tag.objects.get_questions_tags(all_questions)
        likes = Like.objects.get_questions_likes_totals(all_questions)
        answer_counts = Answer.objects.get_questions_answers(all_questions)
        all_questions = list(
            zip(all_questions, question_tags, likes, answer_counts))
        return all_questions

    def get_hot(self):
        all_questions = Question.objects.annotate(sum=Coalesce(Sum(Case(When(common_content__like__state=True, then=Value(
            1)), When(common_content__like__state=False, then=Value(-1)))), 0)).order_by('-sum', '-creation_date')
        question_tags = Tag.objects.get_questions_tags(all_questions)
        likes = Like.objects.get_questions_likes_totals(all_questions)
        answer_counts = Answer.objects.get_questions_answers(all_questions)
        all_questions = list(
            zip(all_questions, question_tags, likes, answer_counts))
        return all_questions

    def get_by_tag(self, tag_name):
        all_questions = Question.objects.order_by(
            '-creation_date').filter(tags__name__iexact=tag_name)
        question_tags = Tag.objects.get_questions_tags(all_questions)
        likes = Like.objects.get_questions_likes_totals(all_questions)
        answer_counts = Answer.objects.get_questions_answers(all_questions)
        all_questions = list(
            zip(all_questions, question_tags, likes, answer_counts))
        return all_questions


class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    common_content = models.OneToOneField(
        'CommonContent', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')
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
    def get_question_answers(self, question):
        answer_count = question.answer_set.all().count()
        return answer_count

    def get_questions_answers(self, questions):
        answer_count_list = list()
        for question in questions:
            answer_count_list.append(self.get_question_answers(question))
        return answer_count_list


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
