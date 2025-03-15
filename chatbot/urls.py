from django.urls import path
from . import views

urlpatterns = [
    path('chattwilio/', views.chattwilio, name='chattwilio'),
    path('chatweb/', views.chatweb, name='chatweb')
]