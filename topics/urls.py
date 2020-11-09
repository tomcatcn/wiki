from django.conf.urls import url
from topics.views import *
urlpatterns = [
    url('^/(?P<username>\w+)$',topics_view),
    url('^/(?P<username>\w+)',topics_view),

]