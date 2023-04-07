from dj_rest_auth.registration.views import ResendEmailVerificationView

from django.contrib import admin
from django.urls import path, include, re_path

from django_base.views import EmailVerification, CustomRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', CustomRegisterView.as_view(), name='rest_register'),

    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('dj-rest-auth/resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    re_path("signup/account-confirm-email/(?P<key>[\s\d\w().+-_',:&]+)/$", EmailVerification.as_view(), name='account_confirm_email'),
]
