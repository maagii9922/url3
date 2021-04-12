
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
        # for entry in incoming_massege()
        return HttpResponse(incoming_massege.object)
