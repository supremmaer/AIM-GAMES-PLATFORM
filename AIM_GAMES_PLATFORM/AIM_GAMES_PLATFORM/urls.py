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
from django.contrib.auth import views as auth_views

#Aqui ponemos las rutas
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('paypal', include('paypal.standard.ipn.urls')),
    path('pagar_paypal', pagarPaypal, name='pagarPaypal' ),
    path('payment_done', payment_done, name='payment_done'),
    path('payment_canceled', payment_canceled, name='payment_canceled'),
    path('loginRedir',loginRedir),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
    path("logout/", auth_views.auth_logout, name="logout"),
    # path('accounts/login/',LoginView.as_view(template_name='accounts/login.html')),
    path('signup',signup,name='signup')

]
