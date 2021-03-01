"""fuel URL Configuration

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
from django.urls import path
from django.conf.urls import include
from fuelsite import views as fuel_views

urlpatterns = [
    path('', fuel_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('test/', fuel_views.test_vue, name='test'),
    path('about/', fuel_views.about, name='about'),
    path('org_data/', fuel_views.org_data, name='org_data'),
    path('public/', fuel_views.public, name='public'),
]
