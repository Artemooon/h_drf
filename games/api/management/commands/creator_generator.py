import random

from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Creator


class Command(BaseCommand):
    help = 'Add randoms games to DB'

    def add_arguments(self, parser):
        parser.add_argument('fakecreators', nargs='?', type=int, default=10)

    def handle(self, *args, **options):
        fake = Faker(['uk_UA'])
        for _ in range(options['fakecreators']):
            creator_rating = random.randint(1, 100)
            creator_name = fake.paragraph(nb_sentences=1)
            creator_logo_url = fake.domain_name()

            Creator.objects.create(name=creator_name, rating=creator_rating,
                                   logo_url=creator_logo_url)

        self.stdout.write(self.style.SUCCESS('Successfully created %s creators' % options['fakecreators']))
