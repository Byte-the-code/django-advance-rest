from django.urls import path, include, re_path

from users.views import UserDocumentationView, UserDocumentationAdminView

urlpatterns = [
    path('documentation/', UserDocumentationView.as_view(), name='user_documentation'),
    path('admin-documentation/', UserDocumentationAdminView.as_view(), name='user_documentation_admin'),
]
