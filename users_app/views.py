from django.shortcuts import render, HttpResponse, redirect
from users_app.models import User
from django.contrib.auth.views import auth_login
from story_app.models import Story

def login (request) :

    context = {}

    if request.method == "POST" :
        email = request.POST['email'] 
        password = request.POST['password'] 

        user = User.login(email=email,password=password)

        if user['errors'] : 
            context['error'] = user['errors']
        else : 
            user = user['user']
            auth_login(request,user)
            return redirect('home')

    return render(request,'login.html',context)


def register (request) : 
    context = {}

    if request.method == "POST" : 
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(
            full_name = full_name,
            email = email,
            password = password,
        )

        if 'img' in request.FILES : 
            picture = request.FILES['img']
            user.picture = picture

        user.save()

        auth_login(request,user)

        return redirect('home')

    return render(request,'register.html',context)


def users (request) : 

    
    stories = Story.objects.order_by('-created_at')
    users = []
    for i in stories : 
        if i.user not in users : 
            users.append(i.user)

    context = {
        'users' : users
    }

    return context