from django.shortcuts import render, redirect
from .forms import UserSignupForm, UserUpdateForm
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
# Create your views here.


class UserSignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Signed up successfully")
        return super().form_valid(form)


class UserSignInView(LoginView):
    template_name = "accounts/signin.html"

    def get_success_url(self):
        messages.success(self.request, "Signed in successfully")
        return reverse_lazy("home")


class UserLogoutView(LogoutView):

    def get_success_url(self):
        messages.info(self.request, "Logged out successfully")
        return reverse_lazy("home")


class UserProfileView(View):
    template_name = "accounts/profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Profile updated Successfully")
            return redirect("profile")
        return render(request, self.template_name, {"form": form})
