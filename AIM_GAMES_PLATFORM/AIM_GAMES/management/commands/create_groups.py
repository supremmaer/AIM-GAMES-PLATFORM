import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class Command(BaseCommand):

    def handle(self, *args, **options):
        #Creación de grupos
        freelancer, created = Group.objects.get_or_create(name='Freelancer')
        business, created = Group.objects.get_or_create(name='Business')
        management, created = Group.objects.get_or_create(name='Management')

        #Obtener grupos (para setear permisos si los grupos ya han sido creados)
        freelancer = Group.objects.get(name='Freelancer')
        business = Group.objects.get(name='Business')
        management = Group.objects.get(name='Management')

        groups = Group.objects.all().values()

        for g in groups:
            print(g)

        #Otorgar permisos (esto se puede resumir con bucles)
        can_add_curriculum = Permission.objects.get(name='Can add curriculum')
        freelancer.permissions.add(can_add_curriculum)

        print("Created default group and permissions.")