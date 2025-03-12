from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

from django import forms
from .models import FarmerProfile
#
# class FarmerProfileForm(forms.ModelForm):
#     class Meta:
#         model = FarmerProfile
#         fields = [
#             'land_area', 'crop_type', 'farming_practices', 'soil_type',
#             'irrigation_method', 'fertilizer_usage', 'cover_crops',
#             'tillage_practices', 'carbon_credits', 'address', 'state', 'district'
#         ]
#         widgets = {
#             'address': forms.Textarea(attrs={'rows': 2}),
#             'carbon_credits': forms.NumberInput(attrs={'step': '0.01'}),
#         }
#
#
# from django import forms
# from .models import FarmerProfile

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = [
            'land_area', 'crop_type', 'farming_practices', 'soil_type',
            'irrigation_method', 'fertilizer_usage', 'cover_crops',
            'tillage_practices', 'carbon_credits', 'address', 'state', 'district'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
        }


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')

        if not video:
            raise forms.ValidationError("No video file uploaded!")

        # ✅ Validate file size (e.g., max 50MB)
        max_size = 200 * 1024 * 1024  # 50MB
        if video.size > max_size:
            raise forms.ValidationError("File size exceeds the 50MB limit!")

        # ✅ Validate file type (only MP4, AVI, MKV, MOV)
        valid_extensions = ['mp4', 'avi', 'mkv', 'mov']
        if not video.name.split('.')[-1].lower() in valid_extensions:
            raise forms.ValidationError("Invalid file format! Only MP4, AVI, MKV, and MOV are allowed.")

        return video
