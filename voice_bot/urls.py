from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='views.upload'),
    path('test/', views.test, name='test'),
]
