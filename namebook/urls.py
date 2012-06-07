from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^register$',  'namebook.views.register_yssy'),
                       (r'^label_entity_types$',  'namebook.views.label_entity_types'),
                       )
