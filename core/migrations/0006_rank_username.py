# Generated by Django 3.1.7 on 2021-04-01 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rank_globalranking'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='username',
            field=models.CharField(default='', max_length=64),
        ),
    ]