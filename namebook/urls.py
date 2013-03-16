from django.conf.urls import patterns

urlpatterns = patterns('',
                       (r'^register$',  'namebook.views.register_yssy'),
                       (r'^label_entity_types$',  'namebook.views.label_entity_types'),
                       )
