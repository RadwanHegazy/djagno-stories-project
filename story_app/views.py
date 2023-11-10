from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users_app.models import User
from .models import Story
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4

@login_required
def home (request) : 

    return render(request,'home.html')


@login_required
def status (request, useruuid) : 
    get_user = get_object_or_404(User,uuid=useruuid)
    context = {
        'current_user' : get_user 
    }

    if Story.objects.filter(user=get_user).count() == 0 : 
        return redirect('home')
    
    if 'api' in request.GET :
        stories = Story.objects.filter(user=get_user)


        for s in stories : 
            if request.user not in s.viewers.all() :
                s.viewers.add(request.user)

        json_data = list()
        for story in stories : json_data.append(story.get_json_data())

        return JsonResponse(json_data,safe=False)
    
    if 'del' in request.GET :
        del_status = request.GET['del']
        
        status = get_object_or_404(Story,uuid=del_status)
        status_owner = status.user
        
        if status_owner == request.user : 
            status.delete()
            if Story.objects.filter(user=status_owner).count() >= 1 :
                return redirect('status',status_owner.uuid)
            return redirect('home')
        return redirect('status',status_owner.uuid)

    return render(request,'status.html',context)


@login_required
@csrf_exempt
def upload_status (request) : 

    if request.method == "POST" : 
        imgs = request.FILES.getlist('img')
        videos = request.FILES.getlist('video')
        
        for i in imgs : 
            Story.objects.create(
                image = i,
                user = request.user,
            )
        
        for i in videos : 
            Story.objects.create(
                video = i,
                user = request.user,
            )
        
        return HttpResponse(request.user.uuid)

    return render(request,'upload.html')


