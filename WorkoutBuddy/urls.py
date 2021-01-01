"""WorkoutBuddy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('find',views.find,name='find'),
    path('about',views.about,name='about'),
    path('excercise_guide',views.excercise_guide,name='excercise_guide'),
    path('accounts/',include('uniauth.urls.cas_only', namespace='uniauth')),
    path('database/',include('buddyrequest.urls')),
    path('partners/',include('buddyrequest.urls')),
    path('contacts/',views.contacts,name='contacts')
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
