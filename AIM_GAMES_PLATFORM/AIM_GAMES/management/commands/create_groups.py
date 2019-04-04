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
        can_add_graphic_engine = Permission.objects.get(name='Can add graphic engine')
        can_edit_graphic_engine = Permission.objects.get(name='Can change graphic engine')
        can_delete_graphic_engine = Permission.objects.get(name='Can delete graphic engine')
        can_view_graphic_engine = Permission.objects.get(name='Can view graphic engine')
        can_add_tag = Permission.objects.get(name='Can add tag')
        can_edit_tag = Permission.objects.get(name='Can change tag')
        can_delete_tag = Permission.objects.get(name='Can delete tag')
        can_view_tag = Permission.objects.get(name='Can view tag')
        freelancer.permissions.add(can_add_curriculum)
        management.permissions.add(can_add_graphic_engine)
        management.permissions.add(can_edit_graphic_engine)
        management.permissions.add(can_delete_graphic_engine)
        management.permissions.add(can_view_graphic_engine)
        management.permissions.add(can_add_tag)
        management.permissions.add(can_edit_tag)
        management.permissions.add(can_delete_tag)
        management.permissions.add(can_view_tag)

        print("Created default group and permissions.")