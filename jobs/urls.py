from django.urls import path
from . import views


urlpatterns = [
    path("", views.list_job, name="list_job"),
]