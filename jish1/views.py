
from django.http import HttpResponse
from django.views import generic

def home(request):
    return HttpResponse("hello")

class Botview(generic.View):
    def get(self,request, *args,**kwargs):
        print(request)
        return HttpResponse("req " + str(request))
        
 