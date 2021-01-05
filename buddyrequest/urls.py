from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.database,name='database'),
    path('profile/<int:request_id>',views.profile,name='profile'),
    path('matches',views.matches,name='matches'),
    path('<int:partner_id>',views.partner_match,name='partner_match'),
    path('remove',views.remove,name='remove'),
    path('details', views.partner,name='partner'),
    path('remove_partner', views.remove_partner,name = 'remove_partner')
]
