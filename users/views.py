from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("signup_success")
    template_name = "users/reg.html"

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return


class SignupSuccess(TemplateView):
    template_name = "users/reg_done.html"
