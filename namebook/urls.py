from django.conf.urls import url
from namebook import views

urlpatterns = [
    url(r'^register$', views.register_yssy),
    url(r'^label_entity_types$', views.label_entity_types, name='club_label_entity_types'),
]
