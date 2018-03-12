from django.urls import path, re_path, include

from . import views

app_name = 'user'
urlpatterns = [
    path('state/', views.state, name='state'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reset/', views.reset, name='reset'),
    re_path(r'^favorite/((?P<type>\d+)/(?P<id>\d+)/)?$', views.Favorite.favorite, name='favorite'),
    re_path(r'^flawbook/((?P<type>\d+)/(?P<id>\d+)/)?$', views.Flawbook.flawbook, name='flawbook'),
    path('weakness/', views.Flawbook.getWeakness, name='weakness')
]