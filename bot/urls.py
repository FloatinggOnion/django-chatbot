from django.urls import path
from .views import chatbot, register, login, logout

urlpatterns = [
    path('', chatbot, name='home'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('logout', logout, name='logout'),
]