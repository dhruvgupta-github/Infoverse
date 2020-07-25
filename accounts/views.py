from django.shortcuts import render 

# reverse lazy is used in case someone is logged_in/logged_out where they should go
from django.urls import reverse_lazy

from accounts import forms

from django.views.generic import CreateView


# Create your views here.

class SignUp(CreateView):
    form_class= forms.UserCreateForm

    # this means after hitting submit they will be transferred to the login page
    success_url = reverse_lazy('login')

    template_name='accounts/signup.html'

