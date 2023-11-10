from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json



class MainSocket (WebsocketConsumer) : 
    
    def connect(self):
        
        # self.user = self.scope['user']

        self.GROUP_NAME = 'MAIN'

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME, self.channel_name
        )
        # if self.user.is_authenticated 
        # else :
        #     self.close()

    
    def close(self, code):
        pass

    def receive(self, text_data):
        print('recived data : ', text_data)
        pass


    def get_msg (self, msg) : 
        self.send(text_data=json.dumps(msg['data']))