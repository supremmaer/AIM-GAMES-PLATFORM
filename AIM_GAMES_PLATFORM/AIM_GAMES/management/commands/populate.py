import logging

from django.db import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from AIM_GAMES.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        tag = Tag(title='Very good tag')
        tag.save()
        tag2 = Tag(title='Very good tag2')
        tag2.save()
        tag3 = Tag.objects.get_or_create(title='Very good tag3')

        graphicEngine1 = GraphicEngine(title='graphicEngine1')
        graphicEngine1.save()
        graphicEngine2 = GraphicEngine(title='graphicEngine2')
        graphicEngine2.save()
        graphicEngine3 = GraphicEngine(title='graphicEngine3')
        graphicEngine3.save()

        url1 = URL(uri='http://www.funcage.com/blog/wp-content/uploads/2013/11/Random-Photoshopped-Pictures-006.jpg')
        url1.save()
        url2 = URL(uri='http://www.funcage.com/blog/wp-content/uploads/2013/11/Random-Photoshopped-Pictures-006.jpg')
        url2.save()
        url3 = URL(uri='http://www.funcage.com/blog/wp-content/uploads/2013/11/Random-Photoshopped-Pictures-006.jpg')
        url3.save()
        url4 = URL(uri='http://www.funcage.com/blog/wp-content/uploads/2013/11/Random-Photoshopped-Pictures-006.jpg')
        url4.save()
        url5 = URL(uri='http://www.funcage.com/blog/wp-content/uploads/2013/11/Random-Photoshopped-Pictures-006.jpg')
        url5.save()
        url6 = URL(uri='http://www.funcage.com/blog/wp-content/uploads/2013/11/Random-Photoshopped-Pictures-006.jpg')
        url6.save()

        superAdmin = User.objects.create_superuser(username='root',email='',password='toor')
        user1 = User.objects.create_user(username='freelancer1', password='estoesuntest')
        user2 = User.objects.create_user(username='freelancer2', password='estoesuntest')
        user3 = User.objects.create_user(username='freelancer3', password='estoesuntest')
        user4 = User.objects.create_user(username='business1', password='estoesuntest')
        user5 = User.objects.create_user(username='business2', password='estoesuntest')
        user6 = User.objects.create_user(username='business3', password='estoesuntest')
        
        profile1= Profile(user=user1, name='freelancer1', surname='surf1', email='freelance1@test.com', city='city1', 
            postalCode='code1', idCardNumber='number1', dateOfBirth='2012-12-12 00:00', phoneNumber='phone1',photo=url1)
        profile1.save()
        profile2= Profile(user=user2, name='freelancer2', surname='surf2', email='freelance2@test.com', city='city2', 
            postalCode='code2', idCardNumber='number2', dateOfBirth='2012-12-12 00:00', phoneNumber='phone2',photo=url2)
        profile2.save()
        profile3= Profile(user=user3, name='freelancer3', surname='surf3', email='freelance1@test.com', city='city3', 
            postalCode='code3', idCardNumber='number3', dateOfBirth='2012-12-12 00:00', phoneNumber='phone3',photo=url3)
        profile3.save()
        profile4= Profile(user=user4, name='business1', surname='surb1', email='business1@test.com', city='city4', 
            postalCode='code4', idCardNumber='number4', dateOfBirth='2012-12-12 00:00', phoneNumber='phone4',photo=url4)
        profile4.save()
        profile5= Profile(user=user5, name='business2', surname='surb2', email='business2@test.com', city='city5', 
            postalCode='code5', idCardNumber='number5', dateOfBirth='2012-12-12 00:00', phoneNumber='phone5',photo=url5)
        profile5.save()
        profile6= Profile(user=user6, name='business3', surname='surb3', email='business3@test.com', city='city6', 
            postalCode='code6', idCardNumber='number6', dateOfBirth='2012-12-12 00:00', phoneNumber='phone6',photo=url6)
        profile6.save()

        freelancer1,created = Freelancer.objects.get_or_create(profile=profile1, profession='profession1')
        freelancer2,created = Freelancer.objects.get_or_create(profile=profile2, profession='profession2')
        freelancer3,created = Freelancer.objects.get_or_create(profile=profile3, profession='profession3')
        
        business1,created = Business.objects.get_or_create(profile=profile4, lastPayment='2014-12-12 00:00')
        business2,created = Business.objects.get_or_create(profile=profile5, lastPayment='2014-12-12 00:00')
        business3,created = Business.objects.get_or_create(profile=profile6, lastPayment='2014-12-12 00:00')

        curriculum1,created = Curriculum.objects.get_or_create(freelancer= freelancer1,verified=False)
        curriculum2,created = Curriculum.objects.get_or_create(freelancer= freelancer2,verified=False)
        curriculum3,created = Curriculum.objects.get_or_create(freelancer= freelancer3,verified=True)

        professionalExperience1,created = ProfessionalExperience.objects.get_or_create(curriculum=curriculum1, center='center1', 
            formation='formation1', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url1)
        professionalExperience2,created = ProfessionalExperience.objects.get_or_create(curriculum=curriculum2, center='center2',
            formation='formation2', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url2)
        professionalExperience3,created = ProfessionalExperience.objects.get_or_create(curriculum=curriculum3, center='center3',
            formation='formation3', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url3)

        Formation1,created = Formation.objects.get_or_create(curriculum=curriculum1, center='center1', 
            formation='formation1', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url1)
        Formation2,created = Formation.objects.get_or_create(curriculum=curriculum2, center='center2', 
            formation='formation2', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url2)
        Formation3,created = Formation.objects.get_or_create(curriculum=curriculum3, center='center3', 
            formation='formation3', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url3)
        Formation4,created = Formation.objects.get_or_create(curriculum=curriculum1, center='center1', 
            formation='formation4', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url4)

        graphicEngineExperience1, created = GraphicEngineExperience.objects.get_or_create(curriculum=curriculum1, 
            graphicEngine=graphicEngine1, graphicExperience=90)
        graphicEngineExperience2, created = GraphicEngineExperience.objects.get_or_create(curriculum=curriculum2, 
            graphicEngine=graphicEngine2, graphicExperience=100)
        graphicEngineExperience3, created = GraphicEngineExperience.objects.get_or_create(curriculum=curriculum3, 
            graphicEngine=graphicEngine3, graphicExperience=75)

        html5Showcase1, created = HTML5Showcase.objects.get_or_create(curriculum=curriculum1, embedCode='codecode')
        html5Showcase2, created = HTML5Showcase.objects.get_or_create(curriculum=curriculum2, embedCode='codecode2')
        html5Showcase3, created = HTML5Showcase.objects.get_or_create(curriculum=curriculum3, embedCode='codecode3')

        Aptitude1, created = Aptitude.objects.get_or_create(curriculum=curriculum1, title='title1')
        Aptitude2, created = Aptitude.objects.get_or_create(curriculum=curriculum2, title='title2')
        Aptitude3, created = Aptitude.objects.get_or_create(curriculum=curriculum3, title='title3')

        link1, created = Link.objects.get_or_create(curriculum=curriculum3, url=url1)
        link2, created = Link.objects.get_or_create(curriculum=curriculum3, url=url2)
        link3, created = Link.objects.get_or_create(curriculum=curriculum3, url=url3)

        jobOffer1, created = JobOffer.objects.get_or_create(business=business1, position='position1',experienceRequired='expr1',
        schedule = 'schedule1', salary=20000, ubication='ubitacion1', description='description1', images='image1')
        jobOffer2, created = JobOffer.objects.get_or_create(business=business2, position='position2',experienceRequired='expr2',
        schedule = 'schedule2', salary=20000, ubication='ubitacion2', description='description2', images='image2')
        jobOffer3, created = JobOffer.objects.get_or_create(business=business3, position='position3',experienceRequired='expr3',
        schedule = 'schedule3', salary=20000, ubication='ubitacion3', description='description3', images='image3')

        t=(tag,)
        p=(url1,)
        at=(url3,)
        thread1= Thread()
        thread1.business=business1
        thread1.title='title1'
        thread1.description='description1'
        thread1.save()
        thread1.tags.set(t)    
        thread1.pics.set(p)  
        thread1.attachedFiles.set(at)
        thread1.save()

        thread2= Thread()
        thread2.business=business1
        thread2.title='title2'
        thread2.description='description2'
        thread2.save()
        thread2.tags.set(t)    
        thread2.pics.set(p)  
        thread2.attachedFiles.set(at)
        thread2.save()

        thread3= Thread()
        thread3.business=business1
        thread3.title='title3'
        thread3.description='description3'
        thread3.save()
        thread3.tags.set(t)    
        thread3.pics.set(p)  
        thread3.attachedFiles.set(at)
        thread3.save()

        
        valoration1, created = Valoration.objects.get_or_create(score=3, thread=thread1, business=business1)
        valoration2, created = Valoration.objects.get_or_create(score=3, thread=thread2, business=business1)
        valoration3, created = Valoration.objects.get_or_create(score=3, thread=thread3, business=business1)
        valoration4, created = Valoration.objects.get_or_create(score=5, thread=thread1, business=business2)
        
        response1 = Response()
        response1.business=business1
        response1.thread=thread1
        response1.title='title1'
        response1.description='desctiption1'
        response1.save()
        response1.pics.set(p)
        response1.save()

        response2 = Response()
        response2.business=business2
        response2.thread=thread1
        response2.title='title2'
        response2.description='desctiption2'
        response2.save()
        response2.pics.set(p)
        response2.save()

        response3 = Response()
        response3.business=business1
        response3.thread=thread2
        response3.title='title3'
        response3.description='desctiption3'
        response3.save()
        response3.pics.set(p)
        response3.save()

        print("Database populated.")