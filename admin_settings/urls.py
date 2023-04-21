from django.urls import path

from admin_settings.views import CategoryListAPIView, ColorListAPIView, MeasureUnitApiView,\
    SubCategoryListApiView

urlpatterns = [
    path('colors/', ColorListAPIView.as_view(), name='color'),
    path('measure-units/', MeasureUnitApiView.as_view(), name='color'),
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('subcategories/', SubCategoryListApiView.as_view(), name='categories'),
]