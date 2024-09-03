import random

from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from user.forms import RegisterForm, UserRegisterConfirmForm
from user.models import User


class UserRegister(TemplateView):
    template_name = 'user/register.html'

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            request.session['register_data'] = form.cleaned_data
            code = random.randint(1000000, 9999999)
            request.session['code'] = code

            # form.save(commit=True)
            # send_sms(forms.cleaned_data['username'], code)
            messages.success(request, "SMS xabar tasdiqlash kodi bilan kiritilgan telefon raqamga jo'natildi")
            return redirect('user:register-confirm')

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(UserRegister, self).get_context_data(**kwargs)
        context['form'] = RegisterForm()
        context["title"] = "Ro'yxatdan o'tish"

        return context

class UserRegisterConfirm(TemplateView):
    template_name = 'user/register-confirm.html'

    def dispatch(self, request, *args, **kwargs):
        data = self.request.session.get('register_data')
        if data is None:
            raise Http404

        return super(UserRegisterConfirm, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserRegisterConfirmForm(request, data=request.POST)
        if form.is_valid():
            data = self.request.session.get('register_data')
            del data['confirm']

            user = User(**data)
            user.save()
            messages.success(request, "Muvaffaqiyatli ro'yatdan o'tdingiz")
            request.session['register_data'] = None
            request.session['code'] = None

            return redirect('user:register')

        context = self.get_context_data()
        context['form'] = form

        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        messages.info(self.request, f"code is: {self.request.session.get('code')}")

        context = super(UserRegisterConfirm, self).get_context_data(**kwargs)

        context['form'] = UserRegisterConfirmForm(self.request)
        context['title'] = "Tasdiqlash"
        return context
