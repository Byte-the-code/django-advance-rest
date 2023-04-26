from django.urls import path

from admin_settings.views import ColorListAPIView, ColorCreateAPIView, ColorRetrieveAPIView, \
    ColorUpdateAPIView, ColorDestroyAPIView, MeasureUnitListCreateAPIView, \
    MeasureUnitRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView, \
    SubCategoryListCreateAPIView, SubCategoryRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('colors/', ColorListAPIView.as_view(), name='list_colors'),
    path('colors/create/', ColorCreateAPIView.as_view(), name='create_color'),

    path('colors/detail/<int:pk>/', ColorRetrieveAPIView.as_view(), name='retrieve_color'),
    path('colors/update/<int:pk>/', ColorUpdateAPIView.as_view(), name='delete_color'),
    path('colors/destroy/<int:pk>/', ColorDestroyAPIView.as_view(), name='update_color'),

    # Measure units (generic views mixed)
    path('measure-units/', MeasureUnitListCreateAPIView.as_view(), name='list_create_measure_unit'),
    path('measure-units/<int:pk>/', MeasureUnitRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_destroy_measure_unit'),

    # Categories (generic views mixed)
    path('categories/', CategoryListCreateAPIView.as_view(), name = 'list_create_category'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_destroy_category'),

    path('subcategories/', SubCategoryListCreateAPIView.as_view(), name = 'list_create_sub_category'),
    path('subcategories/<int:pk>/', SubCategoryRetrieveUpdateDestroyAPIView.as_view(), name='retrieve_update_destroy_sub_category'),
]