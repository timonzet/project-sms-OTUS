from django.contrib import admin
from django.urls import path
from .views import (
    IndexTemplateView,
    ShowProfile,
    EditProfile,
    get_service,
    index_page,
    get_sms,
)

app_name = "my_app"


urlpatterns = [
    path("", index_page, name="index"),
    path("get-service/", get_service, name="get-service"),
    path("get-sms/", get_sms, name="get-sms"),
    path("profile/", ShowProfile.as_view(), name="profile"),
    path("profile/edit/<int:pk>/", EditProfile.as_view(), name="profile-edit"),
]
