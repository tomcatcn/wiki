"""wiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from .views import *
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test',test),
    url(r'^api/v1/users',include('users.urls')),
    url(r'^api/v1/tokens',include('wtoken.urls')),
    url(r'^api/v1/topics',include('topics.urls')),
    url(r'^api/v1/messages',include('message.urls')),
    url(r'^api/v1/photos',include('photos.urls')),
]

urlpatterns += static(settings.MEDIA_URI,document_root=settings.MEDIA_ROOT)
