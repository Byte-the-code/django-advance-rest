from django.urls import path

from admin_settings.views import CategoryListAPIView, ColorListAPIView, MeasureUnitListCreateApiView,\
    SubCategoryListApiView, ColorCreateApiView, ColorRetrieveApiView, ColorUpdateApiView,\
    ColorDestroyApiView, MeasureUnitRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('colors/', ColorListAPIView.as_view(), name='color'),
    path('color/create/', ColorCreateApiView.as_view(), name = 'create-color'),
    path('color/detail/<int:pk>/', ColorRetrieveApiView.as_view(), name = 'retrieve-color'),
    path('color/update/<int:pk>/', ColorUpdateApiView.as_view(), name = 'update-color'),
    path('color/destroy/<int:pk>/', ColorDestroyApiView.as_view(), name = 'destroy-color'),

    path('measure-units/', MeasureUnitListCreateApiView.as_view(), name='measure-units'),
    path('measure-units/<int:pk>/', MeasureUnitRetrieveUpdateDestroyAPIView.as_view(), name='measure-units'),

    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('subcategories/', SubCategoryListApiView.as_view(), name='categories'),
]