# Generated by Django 4.0.2 on 2022-02-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='defeats',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='draws',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='goals_conceded',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='goals_difference',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='goals_scored',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
