from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .models import *

def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

from django.http import JsonResponse
from django.views import View

@login_required()
class RegistrationOptionsView(View):
    def get(self, request):
        options = [
            {"type": "Farmer", "url": "/register/farmer/"},
            {"type": "MSME", "url": "/register/msme/"},
            {"type": "Household", "url": "/register/household/"}
        ]
        return JsonResponse({"options": options})


from django.views import View
from django.shortcuts import render

class RegistrationOptionsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/services.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FarmerProfileForm  # Create this form in Step 2
from .models import FarmerProfile

@login_required
def register_farmer(request):
    # Check if the logged-in user already has a FarmerProfile
    if FarmerProfile.objects.filter(user=request.user).exists():
        messages.info(request, "Your application is pending approval, we will get in touch with you soon.\n Thank you for your patience.")
        return redirect('/')  # Redirect to homepage

    if request.method == 'POST':
        form = FarmerProfileForm(request.POST)
        if form.is_valid():
            farmer_profile = form.save(commit=False)
            farmer_profile.user = request.user
            farmer_profile.verification_status = "pending"
            farmer_profile.save()

            # Display success message
            messages.success(request, "Your form has been successfully submitted. Awaiting approval.")
            return redirect('/')  # Redirect to homepage
        else:
            messages.error(request, "There was an error in your submission. Please try again.")
    else:
        form = FarmerProfileForm()

    return render(request, 'users/register_farmer.html', {'form': form})


@login_required()
def register_msme(request):
    return render(request, 'users/register_msme.html')

@login_required()
def register_household(request):
    return render(request, 'users/register_household.html')

@login_required()
def home(request):
    if request.user.is_authenticated:
        return render(request, 'users/home.html')
    return redirect('login')

@login_required
def farmer_registration(request):
    if FarmerProfile.objects.filter(user=request.user).exists():
        messages.info(request, "Your application is pending verification.")
        return redirect('home')  # Redirect to home with message

    if request.method == 'POST':
        form = FarmerProfileForm(request.POST)
        if form.is_valid():
            farmer_profile = form.save(commit=False)
            farmer_profile.user = request.user
            farmer_profile.verification_status = "pending"
            farmer_profile.save()
            messages.success(request, "Your form has been submitted successfully. Awaiting approval.")
            return redirect('home')  # Redirect to home page
        else:
            messages.error(request, "There was an error in your submission. Please try again.")
    else:
        form = FarmerProfileForm()

    return render(request, 'users/register_farmer.html', {'form': form})
#
# @login_required
# def register_farmer(request):
#     # Check if a FarmerProfile already exists for this user
#     if FarmerProfile.objects.filter(user=request.user).exists():
#         messages.info(request, "Your application is pending verification.")
#         return redirect('home')  # Redirect to home with message
#
#     if request.method == 'POST':
#         form = FarmerProfileForm(request.POST)
#         if form.is_valid():
#             farmer_profile = form.save(commit=False)
#             farmer_profile.user = request.user
#             farmer_profile.verification_status = "pending"
#             farmer_profile.save()
#             messages.success(request, "Your form has been submitted successfully. Awaiting approval.")
#             return redirect('home')  # Redirect to home page
#         else:
#             messages.error(request, "There was an error in your submission. Please try again.")
#     else:
#         form = FarmerProfileForm()
#
#     return render(request, 'users/register_farmer.html', {'form': form})