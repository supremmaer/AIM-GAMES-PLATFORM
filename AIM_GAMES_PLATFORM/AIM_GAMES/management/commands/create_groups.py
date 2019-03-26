import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class Command(BaseCommand):

    def handle(self, *args, **options):
        freelancer, created = Group.objects.get_or_create(name='Freelancer')
        business, created = Group.objects.get_or_create(name='Business')



        print("Created default group and permissions.")