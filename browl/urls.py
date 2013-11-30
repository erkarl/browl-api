from django.conf.urls import patterns, include, url
from rest_framework import routers
from apps.posts.views import PostViewSet
from apps.users.views import UserViewSet

from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
                       url(r'^admin/', include(admin.site.urls)),
                       )
