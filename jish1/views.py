
from django.http import HttpResponse
from django.views import generic

def home(request):
    return HttpResponse("hello")
VERIFY_TOKEN='123456'
class Botview(generic.View):
    def get(self,request, *args,**kwargs):
        if self.request.GET['hub.verify_token']==VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

        
 