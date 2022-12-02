from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path(r'', views.MainApi.as_view()),
    path('home/', views.MainApi.as_view()),
]
