from django.conf.urls import url, include

from . import views

app_name = 'user'
urlpatterns = [
    url(r'state/$', views.state, name='state'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^favorite/((?P<type>\d+)/(?P<id>\d+)/)?$', views.Favorite.favorite, name='favorite'),
    url(r'^flawbook/((?P<type>\d+)/(?P<id>\d+)/)?$', views.Flawbook.flawbook, name='flawbook')
]