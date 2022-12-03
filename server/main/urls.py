from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path(r'', views.MainApi.as_view()),
    path('api/get_capacity', views.CapacityApi.as_view()),
    path('api/get_all_capacity', views.AllCapacityApi.as_view()),
]
