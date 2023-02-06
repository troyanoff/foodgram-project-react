from django.core.management.base import BaseCommand
import json
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает объекты и таблиц csv в БД.'

    def handle(self, *args, **kwargs):

        path = 'recipes/ingredients.json'

        with open(path) as json_file:
            data = json.load(json_file)
            for ingr in data:
                ingredient = Ingredient(
                    name=ingr['name'],
                    measurement_unit=ingr['measurement_unit']
                )
                ingredient.save()

        self.stdout.write('Объекты загруженны в базу данных.')
