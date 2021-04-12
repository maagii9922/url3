
from django.http import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
import random
import requests


def home(request):
    return HttpResponse("hello")

PAGE_ACCESS_TOKEN = "EAANZA3YNaNMEBAIW4FYwzrnZA9C3NFwZCwXDaGQUUp6wRes2d0p6HJ6ygwLd8HT5ZC04fV3zMGrF9jp3YTvJMjZCvFHaGgZCcPdV27Dvx06qulupKvZBOQCbsBqX7sRYeyabf5K1BOJV6pKUAmCMfcrZCncNG6Ry3R8JIxaKnz3GNgZDZD"
VERIFY_TOKEN='123456'

class Botview(generic.View):
    def get(self,request, *args,**kwargs):
        if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        incoming_massege=json.loads(self.request.body.decode('utf-8'))


        # return HttpResponse(incoming_massege['object']
        for entry in incoming_massege['entry']:
            # print(entry)
            for m in entry['messaging']:
                # print(m)
                if 'message' in m:
                    # post_facebook_message(m['sender']['id'],m['message']['text'])
                    handleMessage(m['sender']['id'], m['message'])
                else :
                    handlePostback(m['sender']['id'], m['message'])

        return HttpResponse()


jokes = {
    u'холбоо барих': [u"""холбоо барих-1.""", u"""холбоо барих-2."""],
    u'түгээмэл асуулт хариулт': [u"""түгээмэл асуулт хариулт-1.""", u"""түгээмэл асуулт хариулт-2"""],
    u'эхлэх': [u"""эхлэх-1""", u"""эхлэх-2."""]
}



def post_facebook_message(fbid, recevied_message):
    tokens = re.sub(r"[^a-zA-Z0-9А-яӨҮөү,\s]", '', recevied_message).lower()
    joke_text = ''

    for key, value in jokes.items(): 
        if tokens.find(key) >= 0:
            joke_text = random.choice(jokes[key])
    
    if not joke_text:
        joke_text = "Би ойлгосонгүй! Бидэн уруу 'Холбоо барих', 'Түгээмэл асуулт хариулт', 'Эхлэх' гэж илгээнэ үү!"
    

    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {
        'fields': 'first_name,last_name', 'access_token': PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = 'Yo ' + user_details['first_name'] + '..! ' + joke_text


    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    response_msg = json.dumps(
        {"recipient": {"id": fbid}, "message": {"text": joke_text}})
    status = requests.post(post_message_url, headers={
                           "Content-Type": "application/json"}, data=response_msg)

    return HttpResponse(joke_text)


#  Handles messages events
def handleMessage(sender_psid, received_message):
    response = ''
    if "text" in received_message:
        response = "text You sent the message: " + received_message['text'] + ". Now send me an image!"
    callSendAPI(sender_psid, response)
  



# Handles messaging_postbacks events
def handlePostback(sender_psid, received_postback):
    pass



#  Sends response messages via the Send API
def callSendAPI(sender_psid, response):
    request_body = {
        "recipient": {"id": sender_psid}, "message": response
    }
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % PAGE_ACCESS_TOKEN
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=request_body)

  





