from django.db import models
from users_app.models import User
from uuid import uuid4
from django.utils.timezone import datetime, timedelta
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Story (models.Model) : 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default= datetime.now() + timedelta(hours=24) )
    image = models.ImageField(upload_to='stories-images/',null=True,blank=True)
    video = models.FileField(upload_to='stories-videos/',null=True,blank=True)
    uuid = models.UUIDField(null=True,blank=True)
    viewers = models.ManyToManyField(User,related_name='story_views',blank=True)

    def __str__(self) : 
        return f'{self.user.full_name}'
    
    def get_json_data (self) : 
        context = {
            'publisher_uuid' : str(self.user.uuid),
            'uuid'  : str(self.uuid),
            'date'  : naturaltime(self.created_at),
            'views' :self.viewers.exclude(uuid=self.user.uuid).count()
        }


        if self.image :
            context['type'] = 'img'
            context['url'] = self.image.url
        
        elif self.video : 
            context['type'] = 'video'
            context['url'] = self.video.url

        return context




@receiver(post_save, sender=Story)
def CreateChannelLayer (created, instance, **kwargs) : 
    if created :
        sender = instance.user
        data = {
            'full_name' : sender.full_name,
            'uuid' : str(sender.uuid),
            'picture' : sender.picture.url,
        }

        group_name = "MAIN"

        channel_layer = get_channel_layer()

        event = {
            'type':'get_msg',
            'data':data
        }

        async_to_sync(channel_layer.group_send)(
            group_name, event
        )

        print('Send to websoket')

        instance.uuid = uuid4()
        instance.save()