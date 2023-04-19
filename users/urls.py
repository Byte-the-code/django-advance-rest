from django.urls import path, include, re_path

from users.views import UserDocumentationView, UserDocumentationAdminView, UserListView, \
    SellersListView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list-view'),
    path('documentation/', UserDocumentationView.as_view(), name='user_documentation'),
    path('admin-documentation/', UserDocumentationAdminView.as_view(), name='user_documentation_admin'),
    path('sellers/', SellersListView.as_view(), name = 'sellers-list-view'),

]
