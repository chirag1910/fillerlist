# Generated by Django 5.1.1 on 2025-02-07 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0002_anime_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anime',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True, unique=True),
        ),
    ]
