from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse



def index(request):
    #esto es como el controlador/servicios
    return render(request, 'index.html')
