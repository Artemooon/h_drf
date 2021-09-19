import random

from django.core.management.base import BaseCommand
from faker import Faker
from api.models import Game, Creator


class Command(BaseCommand):
    help = 'Add randoms games to DB'

    def add_arguments(self, parser):
        parser.add_argument('fakegames', nargs='?', type=int, default=10)

    def handle(self, *args, **options):
        fake = Faker(['uk_UA'])
        for _ in range(options['fakegames']):
            game_rating = random.randint(1, 100)
            game_name = fake.paragraph(nb_sentences=1)
            game_description = fake.paragraph(nb_sentences=4)
            game_logo_url = fake.domain_name()
            game_creator = Creator.objects.get(id=1)
            Game.objects.create(name=game_name, description=game_description, rating=game_rating,
                                logo_url=game_logo_url, creator=game_creator)
        self.stdout.write(self.style.SUCCESS('Successfully created %s games' % options['fakegames']))
