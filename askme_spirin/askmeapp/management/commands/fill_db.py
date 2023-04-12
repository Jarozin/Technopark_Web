from django.core.management.base import BaseCommand, CommandError
from askmeapp import models
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from random import sample, randint, seed


class Command(BaseCommand):
    help = "Add objects to databse according to ratio"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']
        i = 0
        avatar_images = list()
        for i in range(3):
            avatar_images.append(f"{finders.find('img')}/avatar{i + 1}.png")

        for i in range(1, ratio + 1):
            new_tag = models.Tag(name=f"Tag_{i}")
            models.Tag.objects.bulk_create([new_tag])

            new_user = User(
                username=f"User_{i}", email=f'user_{i}@mail.ru', password='asdqweqwe_123')
            models.User.objects.bulk_create([new_user])

            new_profile = models.Profile(
                user=new_user, avatar=avatar_images[i % 3])
            models.Profile.objects.bulk_create([new_profile])

        for i in range(1, ratio + 1):
            new_questions = list()
            for j in range(1, 11):
                new_question = models.Question(
                    title=f'{(i - 1) * 10 + j} question title', content=f'this is a content for question number {(i - 1) * 10 + j}', user_id=ratio)
                new_questions.append(new_question)
            models.Question.objects.bulk_create(new_questions)
            for j in range(10):
                seed(j * 101)
                tags = sample(range(1, ratio + 1),
                              randint(1, 10 if ratio > 10 else ratio))
                question_tags = list()
                for tag in tags:
                    question_tags.append(models.Tag.objects.get(id=tag))
                if models.Tag.objects.get(id=i) not in question_tags:
                    question_tags.append(models.Tag.objects.get(id=i))
                new_questions[j].tags.set(question_tags)
            new_answers = list()
            for j in range(1, 101):
                new_answer = models.Answer(content=f'content for answer number {j + (i - 1) * 100}', correct=not bool(
                    j % 100), question=new_questions[(j - 1) % 10],  user_id=ratio)
                new_answers.append(new_answer)
            models.Answer.objects.bulk_create(new_answers)

        for i in range(1, ratio + 1):
            new_question_likes = list()
            seed(j * 101)
            question_ids = sample(range(1, ratio * 10), 18)
            for j in range(18):
                new_like = models.QuestionLike(user=models.Profile.objects.get(
                    id=i), state=bool(j % 2), question_id=question_ids[j])
                new_question_likes.append(new_like)
            models.QuestionLike.objects.bulk_create(new_question_likes)

            new_answer_likes = list()
            seed(j * 101)
            answer_ids = sample(range(1, ratio * 100), 182)
            for j in range(182):
                new_like = models.AnswerLike(user=models.Profile.objects.get(
                    id=i), state=bool(j % 2), answer_id=answer_ids[j])
                new_answer_likes.append(new_like)
            models.AnswerLike.objects.bulk_create(new_answer_likes)
