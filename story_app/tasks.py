from .models import Story
from celery import shared_task
from django.utils.timezone import datetime, get_current_timezone
import time


@shared_task(bind=True)
def CheckStories (self) :


    while True :
        for story in Story.objects.all() : 
            if story.expired_at < datetime.now(tz=get_current_timezone()) :
                print(f'user {story.user.full_name} stoy expired and deleted !')
                story.delete()
            print('Not Deleted !')
        time.sleep(60)
