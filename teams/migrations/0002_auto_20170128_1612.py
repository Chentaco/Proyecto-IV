# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jugador',
            options={'ordering': ['team']},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['nombre']},
        ),
        migrations.RenameField(
            model_name='jugador',
            old_name='nombre',
            new_name='nick',
        ),
        migrations.RemoveField(
            model_name='jugador',
            name='nickname',
        ),
        migrations.AddField(
            model_name='jugador',
            name='megusta',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='jugador',
            name='name',
            field=models.CharField(default=datetime.datetime(2017, 1, 28, 16, 11, 50, 813359, tzinfo=utc), max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jugador',
            name='slug',
            field=models.SlugField(default=b'', unique=True),
        ),
        migrations.AddField(
            model_name='team',
            name='direccion',
            field=models.CharField(default=datetime.datetime(2017, 1, 28, 16, 12, 6, 239004, tzinfo=utc), max_length=70),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='slug',
            field=models.SlugField(default=b'', unique=True),
        ),
        migrations.AddField(
            model_name='team',
            name='visitas',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]
