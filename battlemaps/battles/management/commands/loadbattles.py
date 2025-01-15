import os
import json
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from battles.models import Battle


class Command(BaseCommand):
    help = 'Loads initial battle data'

    def handle(self, *args, **options):
        if Battle.objects.exists():
            self.stdout.write('Battles already loaded.')

        with open(os.path.join(settings.BASE_DIR, 'battle_map_data.json')) as f:
            battle_data = json.load(f)
        for battle in battle_data:
            Battle.objects.create(
                name=battle['battle'],
                wiki_link=battle['link'],
                date=battle['date'],
                point=Point(float(battle['latitude']), float(battle['longitude']))
            )
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded battles')
        )
