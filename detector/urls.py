from django.urls import path
from . import views

urlpatterns = [
    path("",views.detector,name="index"),
    path("info/",views.info,name="info"),
    path("url/",views.grover,name="grover"),
    path("current-affair/",views.current_affair,name="current"),
    path("neutralizer/",views.neutralizer,name="neutralizer"),
    path("fb/",views.facebook,name="facebook"),
]

