"""todo_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

from .api import router

v = settings.API_VERSION

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # API
    # Auth endpoints
    url(r'^api/' + v + '/auth/refresh/', refresh_jwt_token, name='refresh_jwt_token'),
    url(r'^api/' + v + '/auth/token/', obtain_jwt_token, name='obtain_jwt_token'),
    # Router endpoints
    url(r'^api/' + v + '/', include(router.urls, namespace='api')),
    # docs
    url(r'^docs/', include('rest_framework_swagger.urls')),

    # only for test purposes
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
