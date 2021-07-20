from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'App'

urlpatterns = [
    path('activityReport/', views.upload_file, name = 'activityReport'),
    path('about/', views.about, name = 'about'),
    path('form/', views.users, name = 'users'),
    path('', views.home, name = 'home')
]