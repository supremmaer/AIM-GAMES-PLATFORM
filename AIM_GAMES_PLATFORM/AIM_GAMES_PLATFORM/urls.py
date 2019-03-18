"""AIM_GAMES_PLATFORM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from AIM_GAMES.views import *
from django.views.generic import TemplateView

#Aqui ponemos las rutas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('paypal', include('paypal.standard.ipn.urls')),
    path('pagar_paypal', pagarPaypal, name='pagarPaypal' ),
    path('payment_done', TemplateView.as_view(template_name= "pets/payment_done.html"), name='payment_done'),
    path('payment_canceled', TemplateView.as_view(template_name= "pets/payment_canceled.html"), name='payment_canceled')

]
