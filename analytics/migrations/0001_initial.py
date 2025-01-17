# Generated by Django 5.1.1 on 2025-01-17 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analytic',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('time', models.DateTimeField()),
            ],
            options={
                'ordering': ['time'],
            },
        ),
    ]