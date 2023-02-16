from django.contrib import admin
from django.urls import path, include

from .views import Login, Register, UserMainPage, Logout, EditUserProfile

urlpatterns = [
    path('login', Login),
    path('register', Register),
    path('user', UserMainPage),
    path('logout', Logout),
    path('user/edit', EditUserProfile),
]
