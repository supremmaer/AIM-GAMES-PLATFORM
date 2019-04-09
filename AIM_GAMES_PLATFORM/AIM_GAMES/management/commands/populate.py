import logging

from django.db import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from AIM_GAMES.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):

        tag = Tag(title='Event')
        tag.save()
        tag2 = Tag(title='Game engine')
        tag2.save()
        tag3 = Tag.objects.get_or_create(title='Software library')

        graphicEngine1 = GraphicEngine(title='Unreal Engine')
        graphicEngine1.save()
        graphicEngine2 = GraphicEngine(title='Unity')
        graphicEngine2.save()
        graphicEngine3 = GraphicEngine(title='RPG Maker')
        graphicEngine3.save()

        url1 = URL(uri='http://www.funcage.com/blog/wp-content/uploads/2013/11/Random-Photoshopped-Pictures-006.jpg')
        url1.save()
        url2 = URL(uri='https://404store.com/2017/08/15/4949794-random-image.jpg')
        url2.save()
        url3 = URL(uri='https://vignette.wikia.nocookie.net/blogclan-2/images/b/b9/Random-image-15.jpg/revision/latest?cb=20160706220047')
        url3.save()
        url4 = URL(uri='https://vignette.wikia.nocookie.net/rpg-maker-wiki/images/7/78/RPGMakerlogo.png/revision/latest?cb=20190109034832')
        url4.save()
        url5 = URL(uri='https://www.linuxadictos.com/wp-content/uploads/unity-logo.jpg')
        url5.save()
        url6 = URL(uri='https://nextn-cdn-nextn.netdna-ssl.com/wp-content/uploads/2016/05/1605-14-Unreal-Engine-1.jpg')
        url6.save()

        User.objects.filter(is_superuser=False).delete()
        #superAdmin = User.objects.create_superuser(username='root',email='',password='toor')
        user1 = User.objects.create_user(username='freelancer1', password='estoesuntest')
        user2 = User.objects.create_user(username='freelancer2', password='estoesuntest')
        user3 = User.objects.create_user(username='freelancer3', password='estoesuntest')
        user4 = User.objects.create_user(username='business1', password='estoesuntest')
        user5 = User.objects.create_user(username='business2', password='estoesuntest')
        user6 = User.objects.create_user(username='business3', password='estoesuntest')
        user7 = User.objects.create_user(username='manager1', password='estoesuntest', is_staff=True)
        user8 = User.objects.create_user(username='manager2', password='estoesuntest', is_staff=True)
        user9 = User.objects.create_user(username='manager3', password='estoesuntest', is_staff=True)

        business_group = Group.objects.get(name='Business')
        freelancer_group = Group.objects.get(name='Freelancer')
        management_group = Group.objects.get(name='Management')

        freelancer_group.user_set.add(user1)
        freelancer_group.user_set.add(user2)
        freelancer_group.user_set.add(user3)
        business_group.user_set.add(user4)
        business_group.user_set.add(user5)
        business_group.user_set.add(user6)
        management_group.user_set.add(user7)
        management_group.user_set.add(user8)
        management_group.user_set.add(user9)

        
        profile1= Profile(user=user1, name='Indiana', surname='Ford', email='indiana@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345678A', dateOfBirth='1990-12-12 00:00', phoneNumber='691000000',photo=url1)
        profile1.save()
        profile2= Profile(user=user2, name='Francisco', surname='Vega', email='francisco@test.com', city='Huelva', 
            postalCode='41008', idCardNumber='12387678B', dateOfBirth='1991-12-12 00:00', phoneNumber='691000002',photo=url2)
        profile2.save()
        profile3= Profile(user=user3, name='Raul', surname='Cuevas', email='raul@test.com', city='Cordoba', 
            postalCode='41008', idCardNumber='12365678C', dateOfBirth='1991-12-12 00:00', phoneNumber='691000003',photo=url3)
        profile3.save()
        profile4= Profile(user=user4, name='TakeTwo', surname='TakeTwo', email='TakeTwo@test.com', city='Barcelona', 
            postalCode='41008', idCardNumber='12340678D', dateOfBirth='2000-12-12 00:00', phoneNumber='691000004',photo=url1)
        profile4.save()
        profile5= Profile(user=user5, name='LigthDemons', surname='LigthDemons', email='LigthDemons@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12347678E', dateOfBirth='2012-12-12 00:00', phoneNumber='691000005',photo=url2)
        profile5.save()
        profile6= Profile(user=user6, name='GreatGames', surname='GreatGames', email='GreatGames@test.com', city='Madrid', 
            postalCode='41008', idCardNumber='12343678F', dateOfBirth='2012-12-12 00:00', phoneNumber='691000006',photo=url3)
        profile6.save()
        profile7= Profile(user=user7, name='Jacinto', surname='Rojo', email='jacinto@test.com', city='Cadiz', 
            postalCode='41008', idCardNumber='12345648G', dateOfBirth='1990-12-12 00:00', phoneNumber='691000007',photo=url1)
        profile7.save()
        profile8= Profile(user=user8, name='Luis', surname='Salazar', email='luis@test.com', city='Madrid', 
            postalCode='41008', idCardNumber='12345658H', dateOfBirth='1985-12-12 00:00', phoneNumber='691000008',photo=url2)
        profile8.save()
        profile9= Profile(user=user9, name='Victor', surname='Blanco', email='victor@test.com', city='Sevilla', 
            postalCode='41008', idCardNumber='12345679I', dateOfBirth='1993-12-12 00:00', phoneNumber='691000009',photo=url3)
        profile9.save()

        freelancer1,created = Freelancer.objects.get_or_create(profile=profile1, profession='Writer')
        freelancer2,created = Freelancer.objects.get_or_create(profile=profile2, profession='Programmer')
        freelancer3,created = Freelancer.objects.get_or_create(profile=profile3, profession='Art Designer')
        
        business1,created = Business.objects.get_or_create(profile=profile4, lastPayment='2014-12-12 00:00')
        business2,created = Business.objects.get_or_create(profile=profile5, lastPayment='2014-12-12 00:00')
        business3,created = Business.objects.get_or_create(profile=profile6, lastPayment='2014-12-12 00:00')

        manager1, created = Manager.objects.get_or_create(profile=profile7)
        manager2, created = Manager.objects.get_or_create(profile=profile8)
        manager3, created = Manager.objects.get_or_create(profile=profile9)

        curriculum1,created = Curriculum.objects.get_or_create(freelancer= freelancer1,verified=False)
        curriculum2,created = Curriculum.objects.get_or_create(freelancer= freelancer2,verified=False)
        curriculum3,created = Curriculum.objects.get_or_create(freelancer= freelancer3,verified=True)

        professionalExperience1,created = ProfessionalExperience.objects.get_or_create(curriculum=curriculum1, center='Nintendo', 
            formation='Co-Writer of Zelda', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url1)
        professionalExperience2,created = ProfessionalExperience.objects.get_or_create(curriculum=curriculum2, center='Ubisoft',
            formation='Worked in Assasins Creed team developer', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url2)
        professionalExperience3,created = ProfessionalExperience.objects.get_or_create(curriculum=curriculum3, center='Blizzard',
            formation='Worked in Starcraft 2 concept art', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url3)

        Formation1,created = Formation.objects.get_or_create(curriculum=curriculum1, center='GAMES RESEARCH CENTER', 
            formation='RPGMAKER course', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url4)
        Formation2,created = Formation.objects.get_or_create(curriculum=curriculum2, center='GAMES RESEARCH CENTER', 
            formation='RPGMAKER developer course', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url4)
        Formation3,created = Formation.objects.get_or_create(curriculum=curriculum3, center='GAMES RESEARCH CENTER', 
            formation='Unity course', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url5)
        Formation4,created = Formation.objects.get_or_create(curriculum=curriculum1, center='GAMES RESEARCH CENTER', 
            formation='Unreal engine course', startDate='2014-12-12 00:00',endDate='2015-12-12 00:00',miniature=url6)

        graphicEngineExperience1, created = GraphicEngineExperience.objects.get_or_create(curriculum=curriculum1, 
            graphicEngine=graphicEngine1, graphicExperience=90)
        graphicEngineExperience2, created = GraphicEngineExperience.objects.get_or_create(curriculum=curriculum2, 
            graphicEngine=graphicEngine2, graphicExperience=100)
        graphicEngineExperience3, created = GraphicEngineExperience.objects.get_or_create(curriculum=curriculum3, 
            graphicEngine=graphicEngine3, graphicExperience=75)

        html5Showcase1, created = HTML5Showcase.objects.get_or_create(curriculum=curriculum1, embedCode='html5Showcase code')
        html5Showcase2, created = HTML5Showcase.objects.get_or_create(curriculum=curriculum2, embedCode='html5Showcase2 code')
        html5Showcase3, created = HTML5Showcase.objects.get_or_create(curriculum=curriculum3, embedCode='html5Showcase3 code')

        Aptitude1, created = Aptitude.objects.get_or_create(curriculum=curriculum1, aptitude='Imaginative')
        Aptitude2, created = Aptitude.objects.get_or_create(curriculum=curriculum2, aptitude='perfectionist')
        Aptitude3, created = Aptitude.objects.get_or_create(curriculum=curriculum3, aptitude='Good art skills')

        link1, created = Link.objects.get_or_create(curriculum=curriculum3, url=url1)
        link2, created = Link.objects.get_or_create(curriculum=curriculum3, url=url2)
        link3, created = Link.objects.get_or_create(curriculum=curriculum3, url=url3)

        jobOffer1, created = JobOffer.objects.get_or_create(business=business1, position='Developer',experienceRequired='Unity',
        schedule = '8am-3pm', salary=20000, ubication='Seville', description='Work in code', images='https://www.linuxadictos.com/wp-content/uploads/unity-logo.jpg')
        jobOffer2, created = JobOffer.objects.get_or_create(business=business2, position='Developer',experienceRequired='None',
        schedule = '8am-3pm', salary=20000, ubication='Seville', description='Good ofert', images='https://www.linuxadictos.com/wp-content/uploads/unity-logo.jpg')
        jobOffer3, created = JobOffer.objects.get_or_create(business=business3, position='Art Designer',experienceRequired='Knows how to use Unity art software library',
        schedule = '8am-3pm', salary=20000, ubication='Seville', description='Create new art', images='http://www.funcage.com/blog/wp-content/uploads/2013/11/Random-Photoshopped-Pictures-006.jpg')

        t=(tag,)
        p=(url1,)
        at=(url3,)
        thread1= Thread()
        thread1.business=business1
        thread1.title='Unity software'
        thread1.description='Here some software'
        thread1.save()
        thread1.tags.set(t)    
        thread1.pics.set(p)  
        thread1.attachedFiles.set(at)
        thread1.save()

        thread2= Thread()
        thread2.business=business1
        thread2.title='Pics library'
        thread2.description='Here one example'
        thread2.save()
        thread2.tags.set(t)    
        thread2.pics.set(p)  
        thread2.attachedFiles.set(at)
        thread2.save()

        thread3= Thread()
        thread3.business=business1
        thread3.title='RPGMAKER course'
        thread3.description='we offert a free course'
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
        response1.title='Its Free'
        response1.description='We can get it online anyway'
        response1.save()
        response1.pics.set(p)
        response1.save()

        response2 = Response()
        response2.business=business2
        response2.thread=thread1
        response2.title='You cheat'
        response2.description='Dont try to get easy money'
        response2.save()
        response2.pics.set(p)
        response2.save()

        response3 = Response()
        response3.business=business1
        response3.thread=thread2
        response3.title='This is too ramdon'
        response3.description='Please delete it'
        response3.save()
        response3.pics.set(p)
        response3.save()

        challenge1, created = Challenge.objects.get_or_create(business=business1, title="Job offert Unity", description="Make a game in only 24h", objectives="A funcional game")
        freelancers1 = (freelancer1, freelancer2)
        challenge1.freelancers.set(freelancers1)
        challenge1.save

        challenge2, created = Challenge.objects.get_or_create(business=business1, title="Future art", description="The winner will get an all-paid vacation", objectives="Surprise us")
        freelancers2 = (freelancer1,)
        challenge2.freelancers.set(freelancers2)
        challenge1.save

        challenge3, created = Challenge.objects.get_or_create(business=business2, title="Unreal antihack", description="Try to make a good antihack system with unreal engine", objectives="The best system will win")
        freelancers3 = (freelancer1, freelancer2, freelancer3)
        challenge3.freelancers.set(freelancers3)
        challenge1.save


        event1, created = Event.objects.get_or_create(manager = manager1, location = "Seville", title="AIMGAME-FEST",description="All you indies developers will be here", moment= "2019-12-12 00:00")
        freelancers1= (freelancer1,)
        businesses1 = (business1,business2)
        event1.freelancers.set(freelancers1)
        event1.companies.set(businesses1)

        event2, created = Event.objects.get_or_create(manager = manager2, location = "Seville", title="Game Camp",description="Want to create some games? you only need to come and have fun", moment= "2019-12-12 00:00")
        freelancers2= (freelancer1,freelancer2)
        businesses2 = (business1,)
        event2.freelancers.set(freelancers2)
        event2.companies.set(businesses2)

        event3, created = Event.objects.get_or_create(manager = manager3, location = "Seville", title="AIM Game EXPO",description="One week of every news of our indies", moment= "2019-12-12 00:00")
        freelancers3= (freelancer1,)
        businesses3 = (business1,)
        event3.freelancers.set(freelancers3)
        event3.companies.set(businesses3)
        
        message1, created = Message.objects.get_or_create(sender=user1, recipient=user2, subject="uwu" ,text="sad")
        message1, created = Message.objects.get_or_create(sender=user2, recipient=user1, subject="owo" ,text="sand dunes")

        print("Database populated.")