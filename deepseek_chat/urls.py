from django.contrib import admin
from django.urls import path
from cbot import views

urlpatterns = [
    path('admin/', admin.site.urls),
    ##path('', views.login, name='login'),
    path('', views.home, name='home'),
    path('chat', views.chat_view, name='chat'),
]