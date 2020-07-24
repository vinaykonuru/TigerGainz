from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.database,name='database'),
    path('profile',views.profile,name='profile'),
    path('matches',views.matches,name='matches'),
    path('partner',views.partner,name='partner')
]
