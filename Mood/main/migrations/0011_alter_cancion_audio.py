# Generated by Django 4.0.6 on 2022-11-18 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_cancion_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancion',
            name='audio',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
