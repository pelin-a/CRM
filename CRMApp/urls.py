from django.urls import path 
from . import views

urlpatterns = [
    path('', views.add_pipeline, name="add_pipeline"),
    path('base', views.base, name="base" )
    
]