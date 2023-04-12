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
        new_bulk = list()
        for i in range(1, ratio + 1):
            new_tag = models.Tag(name = f"Tag_{i}")
            models.Tag.objects.bulk_create([new_tag])

            new_user = User(username = f"User_{i}", email = f'user_{i}@mail.ru', password='asdqweqwe_123')
            models.User.objects.bulk_create([new_user])

            new_profile = models.Profile(user = new_user, avatar=avatar_images[i % 3])
            models.Profile.objects.bulk_create([new_profile])

            new_content = list()
            for j in range(110):
                new_common_content = models.CommonContent(user = new_profile)
                new_content.append(new_common_content)
            models.CommonContent.objects.bulk_create(new_content)

        for i in range(1, ratio + 1):
            new_questions = list()
            for j in range(1, 11):
                new_question = models.Question(title=f'{(i - 1) * 10 + j} question title', content = f'this is a content for question number {(i - 1) * 10 + j}', common_content_id = (i - 1) * 110 + j)
                new_questions.append(new_question)
            models.Question.objects.bulk_create(new_questions)
            for j in range(10):
                seed(j * 101)
                tags = sample(range(1, ratio + 1), randint(1, 10 if ratio > 10 else ratio))
                question_tags = list()
                for tag in tags:
                    question_tags.append(models.Tag.objects.get(id=tag))
                new_questions[j].tags.set(question_tags)
            new_answers = list()
            for j in range(1, 101):
                new_answer = models.Answer(content = f'content for answer number {j + (i - 1) * 100}', correct = not bool(j % 100), question = new_questions[(j - 1) % 10], common_content_id = (i - 1) * 110 + j + 10)
                new_answers.append(new_answer)
            models.Answer.objects.bulk_create(new_answers)

        #TODO: При распределении тэгов каждый тэг присвоить хотя бы один раз
        for i in range(1, ratio + 1):
            new_likes = list()
            seed(j * 101)
            content_numbers = sample(range(1, ratio * 110), 200)
            for j in range(200):
                new_like = models.Like(user = models.Profile.objects.get(id=i), state=bool(j % 2), common_content_id = content_numbers[j])
                new_likes.append(new_like)
            models.Like.objects.bulk_create(new_likes)
