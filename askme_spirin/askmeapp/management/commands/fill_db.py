from django.core.management.base import BaseCommand, CommandError
from askmeapp import models
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders

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
        for i in range(ratio):
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
            ###TODO: поменять коэф для лайков до 200
            new_likes = list()
            for j in range(20):
                new_like = models.Like(user = new_profile, state=bool(j % 2), common_content = new_content[j * 3])
                new_likes.append(new_like)
            models.Like.objects.bulk_create(new_likes)

            new_questions = list()
            for j in range(10):
                new_question = models.Question(title=f'{i * 10 + j} question title', content = f'this is a content for question number {i * 10 + j}', common_content = new_content[j])
                new_questions.append(new_question)
            models.Question.objects.bulk_create(new_questions)
            for j in range(10):
                new_questions[j].tags.set([new_tag])
            new_answers = list()
            for j in range(100):
                new_answer = models.Answer(content = f'content for answer number {j + i * 100}', correct = not bool(j % 100), question = new_questions[j % 10], common_content = new_content[10 + j])
                new_answers.append(new_answer)
            models.Answer.objects.bulk_create(new_answers)
