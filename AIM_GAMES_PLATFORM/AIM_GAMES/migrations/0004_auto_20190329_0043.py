# Generated by Django 2.1.7 on 2019-03-28 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0003_auto_20190329_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professionalexperience',
            name='center',
            field=models.TextField(max_length=50, verbose_name='Centrooo'),
        ),
    ]
