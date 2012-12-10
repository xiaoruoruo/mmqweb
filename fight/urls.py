from django.conf.urls import patterns

urlpatterns = patterns('',
                       (r'^$',  'mmqweb.fight.views.index'),
                       (r'^submit$',  'mmqweb.fight.views.submit'),
                       )
