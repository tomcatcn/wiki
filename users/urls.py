from django.conf.urls import url
from users.views import *
urlpatterns =[
    url('^$',users_view),
    url(r'^/(?P<username>\w+)$',users_view),
    url(r'^/(?P<username>\w+)/avatar$',avatar_view)
]