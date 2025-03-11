from tokenize import group
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, FormView
from .models import BaseRegisterForm, BasicSignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'sign/signup.html'
    success_url = reverse_lazy('users-profile')

    def form_valid(self, form):
        user = form.save()
        common_group = Group.objects.get(name='common')
        user.groups.add(common_group)
        user.save()
        return super().form_valid(form)


# @login_required
# def upgrade_me(request):
#     user = request.user
#     premium_group = Group.objects.get(name='premium')
#     if not request.user.groups.filter(name='premium').exists():
#         premium_group.user_set.add(user)
#     return redirect('users_profile')
