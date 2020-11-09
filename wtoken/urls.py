from django.conf.urls import url
from wtoken.views import *
urlpatterns =[
    url('^$',tokens_view)
]