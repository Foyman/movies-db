from django.urls import path
from . import views

urlpatterns = [path('', views.index, name = 'index'),
               path('entry/<int:bestpic_id>/', views.entry, name = 'entry'),
               path('search/', views.search, name = 'search'),]
