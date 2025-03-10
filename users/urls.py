from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    # path('services/', RegistrationOptionsView, name='services'),
    path('services/', RegistrationOptionsView.as_view(), name='services'),
    path('register/farmer/', register_farmer, name='register_farmer'),
    path('register/msme/', register_msme, name='register_msme'),
    path('register/household/', register_household, name='register_household'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)