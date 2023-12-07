

from django.urls import path
from . import views

urlpatterns = [
    path('', views.form),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('logout', views.logout),
    path('create_post', views.create_post),
    path('delete_post/<int:id>', views.delete_post),
    path('create_comment', views.create_comment),
    path('delete_comment/<int:id>', views.delete_comment),
]