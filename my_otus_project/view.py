from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class IndexTemplateView(UserPassesTestMixin, TemplateView):
    template_name = "index.html"

    login_url = "app_auth:login"

    def test_func(self):
        # Order.objects.filter(...)
        return self.request.user.is_authenticated
