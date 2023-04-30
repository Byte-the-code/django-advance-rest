from django.urls import path

from products.views import MyProductsView, ProductsRetrieveUpdateDestroyView, ProductDistinguisehedView,\
    ProductsListView, BanProductsAdminView


urlpatterns = [
    path('my-products/', MyProductsView.as_view()),
    path('<int:pk>/', ProductsRetrieveUpdateDestroyView.as_view()),
    path('list/', ProductsListView.as_view()),
    path('distinguished/<int:pk>/', ProductDistinguisehedView.as_view()),
    path('ban/<int:pk>/', BanProductsAdminView.as_view()),
]
