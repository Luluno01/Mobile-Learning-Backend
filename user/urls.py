from django.conf.urls import url, include

from . import views

app_name = 'user'
urlpatterns = [
    url(r'state/$', views.state, name='state'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^favorite/$', views.getFavorite, name='get-favorite'),
    url(r'^favorite/add$', views.addFavorite, name='add-favorite'),
    url(r'^favorite/del$', views.delFavorite, name='del-favorite'),
    url(r'^flawbook/$', views.getFlawbook, name='get-flawbook'),
    url(r'^flawbook/add$', views.addFlaw, name='add-flaw'),
    url(r'^flawbook/del$', views.delFlaw, name='del-flaw')
]