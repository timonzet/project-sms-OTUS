import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView, ListView
from VakSmsApi import VakSmsApi
import requests
from .forms import (
    ProfileForm,
)
from .models import ProfileUser, ProfileOperations

api = VakSmsApi(api_key="c230a5896a6e4ab1a743d07a0340fc78")
API = "c230a5896a6e4ab1a743d07a0340fc78"


def get_list_services(country, operator):
    url = f"https://vak-sms.com/api/getCountNumberList/?apiKey={API}&country={country}&operator={operator}&price"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code)


@login_required
def get_service(request):
    if request.method == "POST":
        service = request.POST.get("service")
        print(service)
        url = f"https://vak-sms.com/api/getNumber/?apiKey={API}&service={service}&country=ru&operator=mts"
        response = requests.get(url)
        services = get_list_services(country="ru", operator="mts")
        price = int(services[service]["price"])
        if response.status_code == 200:
            context_service = response.json()
            if context_service.keys() == "error":
                return JsonResponse(
                    {
                        "error": context_service,
                        "price": price,
                    },
                    content_type="application/json",
                )
            else:
                print(context_service)
                operation = ProfileOperations(
                    profile=request.user.profile,
                    tel=context_service["tel"],
                    id_num=context_service["idNum"],
                    status="1",
                )
                operation.save()
                numbers = get_list_numbers(request)
                return JsonResponse(
                    {
                        "tel": context_service["tel"],
                        "id": context_service["idNum"],
                        "price": price,
                        "numbers": numbers,
                    },
                    content_type="application/json",
                )
        else:
            raise Exception(response.status_code)
    else:
        qr = dict(get_list_services(country="ru", operator="mts")).items()

        return render(
            request,
            "my_app/index.html",
            context={
                "services": qr,
            },
        )


def get_list_numbers(request: HttpRequest):
    numbers = ProfileOperations.objects.filter(
        status=ProfileOperations.Status.active, profile=request.user.profile
    ).all()
    numbers_data = list(numbers.values())

    # Проверяем каждое значение на сериализуемость
    for data in numbers_data:
        for key, value in data.items():
            if not isinstance(value, (str, int, float)):
                data[key] = str(value)  # Преобразуем неподдерживаемые типы в строки

    json_data = json.dumps(numbers_data)

    print(json_data)
    return json_data


def get_sms(request: HttpRequest):
    if request.method == "POST":
        id = request.POST.get("id")
        url = f"https://vak-sms.com/api/getSmsCode/?apiKey={API}&idNum={id}"
        response = requests.get(url)
        sms = response.json()
        print(sms, id)
        return JsonResponse(
            {
                "tel": response.json(),
            },
            content_type="application/json",
        )


def index_page(request: HttpRequest):
    qr = dict(get_list_services(country="ru", operator="mts")).items()
    return render(
        request,
        template_name="my_app/index.html",
        context={
            "services": qr,
        },
    )


class IndexTemplateView(TemplateView):
    template_name = "my_app/index.html"
    queryset = dict(get_list_services(country="ru", operator="mts")).items()
    extra_context = {"services": queryset}


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
