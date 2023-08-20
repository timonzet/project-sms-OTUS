from django import forms
from django.contrib.auth.models import User

from .models import ProfileUser


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = "profile_pic", "facebook", "twitter", "instagram", "telegramm", "phone"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            print(name, field)
            field: forms.Field
            widget: forms.Widget = field.widget
            widget.attrs["class"] = "form-control"
            if isinstance(field, forms.CharField):
                print(field.label, type(field.label))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "first_name", "last_name", "email"
