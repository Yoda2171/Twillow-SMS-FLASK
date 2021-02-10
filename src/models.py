import os
from twilio.rest import Client

class Queue:

    def __init__(self):
        self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.client = Client(self.account_sid, self.auth_token)
        self._queue = []
        self._mode = 'FIFO'

    def enqueue(self, item):

        if self.size() == 0:
            message = self.client.messages.create (
                body = str(item["name"]) + ", es su turno",
                from_='+12055578744',
                to='+56 9 6632 7166',
            )          
        
        else:
            message = self.client.messages.create (
                body='Bienvenidos, ' +  str(item["name"]) + " tu tienes " + str(self.size()) + " personas por delante de usted, espere su turno",
                from_='+12055578744',
                to='+56 9 6632 7166',
            )

        self._queue.append(item)

        
        
    
    def dequeue(self):
        
        item = self._queue.pop(0)

        message = self.client.messages.create(
            body= item["name"] + " Muchas Gracias!!, que tengan un buen dia",
            from_ = "+12055578744",
            to = '+56 9 6632 7166',            
            )


    def get_queue(self):

        return self._queue


    def size(self):
        return len(self._queue)
