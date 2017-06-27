from django.conf.urls import url, include

from . import views

app_name = 'user'
urlpatterns = [
    url(r'state/$', views.state, name='state'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^reset/$', views.reset, name='reset'),
]