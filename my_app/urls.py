from django.contrib import admin
from django.urls import path
from .views import (
    IndexTemplateView,
    ShowProfile,
    EditProfile,
)

app_name = "my_app"


urlpatterns = [
    path("", IndexTemplateView.as_view(), name="index"),
    path("profile/", ShowProfile.as_view(), name="profile"),
    path("profile/edit/<int:pk>", EditProfile.as_view(), name="profile-edit"),
]
