# Generated by Django 4.1.6 on 2023-02-14 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_amount_options_alter_favoriterecipe_options_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorited'),
        ),
        migrations.AddConstraint(
            model_name='following',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_follower'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ungredient'),
        ),
        migrations.AddConstraint(
            model_name='recipetag',
            constraint=models.UniqueConstraint(fields=('recipe', 'tag'), name='unique_recipe_tag'),
        ),
        migrations.AddConstraint(
            model_name='shoprecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping'),
        ),
    ]
