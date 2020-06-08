from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('processdata/',views.reqitem,name="reqitem"),
    path('api/',views.apireqitem,name="apirequest")
]
