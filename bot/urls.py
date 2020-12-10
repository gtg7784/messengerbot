from django.conf.urls import url
from . import views

urlpatterns = [
  url('bot/', views.chat, name="chat"),
  url(r'', views.index, name="index")
]
