# Generated by Django 2.1.7 on 2019-03-25 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AIM_GAMES', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='lastPayment',
            field=models.DateTimeField(null=True),
        ),
    ]