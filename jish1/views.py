
from django.http import HttpResponse
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return HttpResponse("hello")

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
                    post_facebook_message(m['sender']['id'],m['message']['text'])
        return HttpResponse("okkkk")


jokes = {
    u'холбоо барих': [u"""холбоо барих-1.""", u"""холбоо барих-2."""],
    u'түгээмэл асуулт хариулт': [u"""түгээмэл асуулт хариулт-1.""", u"""түгээмэл асуулт хариулт-2"""],
    u'эхлэх': [u"""эхлэх-1""", u"""эхлэх-2."""]
}

def post_facebook_message(fbid, recevied_message):
    tokens = re.sub(r"[^a-zA-Z0-9А-я,\s]", '', recevied_message).lower()
    
    joke_text = ''

    for key, value in jokes.items(): 
    if tokens.find(key) >= 0:
        joke_text = random.choice(jokes[key])
    
    if not joke_text:
        print(u"Би ойлгосонгүй! Бидэн уруу '%s', 'Түгээмэл асуулт хариулт', 'Эхлэх' гэж илгээнэ үү!"%("Холбоо барих"))









