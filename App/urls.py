from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'App'

urlpatterns = [
    path('activityReport/', views.upload_file, name = 'activityReport'),
    path('pulseEmailStats/', views.pulseUpdate, name = 'pulseEmailStats'),
    path('internTool/', views.internTool, name = 'internTool'),
    path('internTool/Submitted', views.activate, name = 'activate'),
    path('about/', views.about, name = 'about'),
    path('form/', views.users, name = 'users'),
    path('', views.home, name = 'home')
]