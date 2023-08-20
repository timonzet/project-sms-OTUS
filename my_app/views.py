from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, UpdateView
from VakSmsApi import VakSmsApi
import requests
from .forms import (
    ProfileForm,
)
from .models import ProfileUser

api = VakSmsApi(api_key="c230a5896a6e4ab1a743d07a0340fc78")
API = "c230a5896a6e4ab1a743d07a0340fc78"


def get_list_services(country, operator):
    url = f"https://vak-sms.com/api/getCountNumberList/?apiKey={API}&country={country}&operator={operator}&price"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code)


class IndexTemplateView(TemplateView):
    template_name = "my_app/index.html"
    response = get_list_services(country="ru", operator="mts")

    extra_context = {
        "api_context": dict(response).items(),
    }


class ShowProfile(LoginRequiredMixin, View):
    model = ProfileUser
    template_name = "my_app/profile.html"

    def get(self, request):
        user_form = request.user
        profile = ProfileUser.objects.get(user_id=user_form.pk)

        context = {
            "user_form": user_form,
            "profile": profile,
        }
        return render(
            request=request, template_name=self.template_name, context=context
        )


class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = "my_app/profile_edit.html"
    model = ProfileUser
    form_class = ProfileForm

    def get_success_url(self):
        return reverse("my_app:profile")


@login_required
def get_service(request: HttpRequest, service, balance: int) -> HttpResponse:
    url = f"https://vak-sms.com/api/getNumber/?apiKey={API}&service={service}&country=ru&operator=mts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code)
