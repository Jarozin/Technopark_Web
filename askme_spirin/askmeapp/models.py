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

class LikeManager(models.Manager):
    def get_question_likes_total(question):
        pass

    def get_questions_likes_totals(questions):
        pass


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
    def get_question_tags(question):
        tags_pk = question.tag
        tags = list()
        for pk in tags_pk:
            new_tag = Tag.objects.get(id=pk)
            tags.append(new_tag)
        return tags

    def get_questions_tags(questions):
        questions_tags = list()
        for question in questions:
            tags = TagManager.get_question_tags(question)
            questions_tags.append(tags)
        return tags

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
    def get_tag(tag):
        return Question.objects.filter(tag__contains=tag)

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
    avatar = models.ImageField(upload_to ='uploads/')

    def __str__(self):
        return self.user.get_username()


class Answer(models.Model):
    content = models.TextField()
    correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    common_content = models.OneToOneField(
        'CommonContent', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:40]
