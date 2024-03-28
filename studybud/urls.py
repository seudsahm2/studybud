from django.contrib import admin
from django.urls import path, include # this include is added to include paths from urls.py file in apps
from django.http import HttpResponse

'''
we can write these functions directly from in this folder


def home(request):
    return HttpResponse('Home page')

def room(request):
    return HttpResponse('Room')

'''

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',home),  commented because we moved them to urls.py file in apps
    #path('room/', room),

    path('',include('base.urls')) # include the urls file in base folder

    
]
