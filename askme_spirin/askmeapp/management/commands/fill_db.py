from django.core.management.base import BaseCommand, CommandError
from askmeapp import models

class Command(BaseCommand):
    help = "Add objects to databse according to ratio"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)


    def handle(self, *args, **options):
        ratio = options['ratio']
        i = 0
        for i in range(ratio):
            new_tag = models.Tag(name = f"Tag_{i}")
            new_tag.save()
