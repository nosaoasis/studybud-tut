from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
from django.db.models import Q
from .forms import RoomForm

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('base:home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, f"{username} not found.")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'Username or Password does not exist.')
    context = {'page': page}
    return render(request, "base_app/login_register.html", context)


def logoutPage(request):
    logout(request)
    return redirect('base:home')


def register_user(request):
    page = 'register'
    form = UserCreationForm
    if request.method == "POST":
      form = UserCreationForm(request.POST)
      if form.is_valid():
        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        login(request, user)
        return redirect('base:home')
      else:
        messages.error(request, "An error occurred.")
    context = {
        'page': page,
        'form': form
    }
    return render(request, 'base_app/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        'title': 'Study Buddy',
        'content': 'Study Physics and Web velopment',
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count
    }
    return render(request, 'base_app/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=int(pk))
    conversations = room.message_set.all().order_by('-created')

    if request.method == "POST":
      message = Message.objects.create(
        user = request.user,
        room = room,
        body = request.POST.get('message_content')
      )
      return redirect('base:room', pk=room.id)

    context = {
        'room': room,
        'conversations': conversations
    }
    return render(request, 'base_app/room.html', context)


@login_required(login_url="base:login")
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base:home')
    context = {'form': form}
    return render(request, 'base_app/room_form.html', context)


@login_required(login_url="base:login")
def update_room(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)

    if request.user == room.host:
        return HttpResponse("You're not permitted to continue with")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('base:home')

    context = {'form': form}
    return render(request, 'base_app/room_form.html', context)


@login_required(login_url="base:login")
def delete_room(request, pk):
    room = Room.objects.get(id=int(pk))
    return HttpResponse("You're not permitted to continue with")
    if request.method == "POST":
        room.delete()
        return redirect('base:home')
    return render(request, 'base_app/delete.html', {'obj': room})
