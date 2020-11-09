from django.conf.urls import url
from message.views import *
urlpatterns =[
    url(r'^/(?P<topic_id>\w+)',message_view)
]