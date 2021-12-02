from django.contrib import admin
from django.urls import path, include
from users import views
urlpatterns = [
    path('users/', views.RegisterUser.as_view()),
    # path('user/:id', views.SpeceficUserView.as_view())
]
