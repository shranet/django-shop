from django import forms
from django.core.exceptions import ValidationError

from user.models import User


class RegisterForm(forms.ModelForm):
    confirm = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        data = super().clean()

        if data.get('password') != data.get('confirm'):
            raise ValidationError({
                "confirm": "Parollar bir xil emas"
            })

        return data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm']
        widgets = {
            'password': forms.PasswordInput
        }


class UserRegisterConfirmForm(forms.Form):
    code = forms.CharField(max_length=10)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_code(self):
        value = self.cleaned_data.get('code')
        code = self.request.session.get('code')
        if value != str(code):
            raise ValidationError("Kiritilgan kod noto'g'ri")

        return value


