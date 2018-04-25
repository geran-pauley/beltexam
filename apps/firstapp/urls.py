from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^quotes$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addquote$', views.addquote),
    url(r'^addfav/(?P<id>\d+)$', views.addfav),
    url(r'^removefav/(?P<id>\d+)$', views.removefav),
    url(r'^users/(?P<id>\d+)$', views.users),
]
