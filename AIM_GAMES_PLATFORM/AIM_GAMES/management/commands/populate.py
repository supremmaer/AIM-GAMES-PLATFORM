import logging

from django.db import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from AIM_GAMES.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        tag = Tag(title='Very good tag')
        tag.save()
        
        print("Database populated.")