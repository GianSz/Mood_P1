# Generated by Django 4.0.6 on 2022-08-16 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_cancion_audio_alter_cancion_frecuencia_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancion',
            name='duracion',
            field=models.TimeField(),
        ),
    ]
