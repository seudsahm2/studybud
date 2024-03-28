from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage, name = "login"),
    path('logout/',views.logoutUser, name = "logout"),
    path('register/',views.registerPage, name = "register"),

    path('',views.home, name="home"),
    #path('room/', views.room, name="room"), just simple routing
    path('room/<str:pk>/', views.room, name="room"), #dynamic url routing  ->  passing the id to the URL
    # but one problem is that if i edit the url above(room) to other name, i have to change all others which are in other files
    # to solve this, in the other files refer this link by its name attribute
    # then whether you change the url or not, it does not matter you do not have to change it in the other files
    # it always refer to this url. see the code in the home.html file
    path('profile/<str:pk>/',views.userProfile, name="user-profile"),
    
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
]