from django.conf.urls import url
from fight import views

urlpatterns = [
    url(r'^$',  views.index),
    url(r'^submit$',  views.submit),
]
