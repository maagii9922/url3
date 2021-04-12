
from django.urls import path
from .views import home,Botview

urlpatterns = [
    path('',home),
    path('webhook',Botview.as_view())
]