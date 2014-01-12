from django.conf.urls import patterns

urlpatterns = patterns('',
                       (r'^$',  'fight.views.index'),
                       (r'^submit$',  'fight.views.submit'),
                       )
