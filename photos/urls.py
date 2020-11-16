from django.conf.urls import url
from photos.views import *

urlpatterns =[
    url(r'^/(?P<username>\w+)$',photos_view),
    url(r'^/(?P<username>\w+)/picture$',upload_view),
]