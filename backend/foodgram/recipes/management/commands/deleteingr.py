from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Удаляет объекты из БД.'

    def handle(self, *args, **kwargs):

        ings = Ingredient.objects.all()
        ings.delete()

        self.stdout.write('Объекты удалены из базы данных.')