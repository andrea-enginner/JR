# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import views
from django.contrib import admin
from django.urls import path, include  # add this


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),             
    path('accounts/', include('django.contrib.auth.urls')),  
  #  path('register/', views.register, name='register'),    
   
    path('', include('apps.registro.urls')),  
    path('marketplace/', include('apps.marketplace.urls')),  
]
