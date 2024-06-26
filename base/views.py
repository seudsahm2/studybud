from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm

#rooms = [
#    {'id':1, 'name':'lets learn python'},
#    {'id':2, 'name':'design with me'},
#    {'id':3, 'name':'front end developers'},
#]

def loginPage(request): # do not use the name login, it will clash with the built in login function
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(username)
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')


    context = {'page':page}    
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm (request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')

    return render(request, 'base/login_register.html',{'form':form})
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
         #this is for the database and the above rooms list is overridden by this list from the database whether it is commented or not
    #return render(request,'home.html', {'rooms':rooms})  you can do this way or
    topic = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
   
    context = {'rooms':rooms,'topics':topic,'room_count':room_count ,'room_messages':room_messages}  # like this
    return render(request,'base/home.html', context)


    #return HttpResponse('Home page')  to return HttpResponse

def room(request,pk): #argument for passing the id in the urls.py for dynamic url routing
    # check in the browser by adding numbers or string characters  after the url for room like this 127.0.0.1:8000/room/2   or 127.0.0.1:8000/room/abc or else
    # now if you press the link in the home.html it also opens the /room site with id of the link as a dynamic url
    # hence the id is routed, we can access it here to reveal what is inside the id

 #   room = None
 #   for i in rooms:
 #       if i['id'] == int(pk): # we convert it to int because the routed url is treated as string (because we set it like that)
 #           room = i
 
 # the above 4 lines are commented to do with the database
    room = Room.objects.get(id=pk) #get method gets one item
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method =='POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')

        )
        
        room.participants.add(request.user)
        return redirect('room',pk = room.id)

    context = {'room' : room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context) 
    #return HttpResponse('Room')

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    context = {'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createRoom(request):
    form =RoomForm()
    if request.method == 'POST':
       # print(request.POST) SEE ITS EFFECT ON THE TERMINAL
       # but we user this way
       form = RoomForm(request.POST)
       if form.is_valid():
        form.save()
        return redirect('home')

        

    context= {'form':form}
    return render(request, 'base/room_form.html',context)
@login_required(login_url='login')
def updateRoom(request,pk): # pk is to choose which element are we updating
    room = Room.objects.get(id=pk)
    form= RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('you are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('you are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


