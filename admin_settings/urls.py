from rest_framework.routers import DefaultRouter

from django.urls import path, include

from admin_settings.views import ColorViewSet, MeasureUnitViewSet, CategoryViewSet, SubCategoryViewSet

router = DefaultRouter()
router.register('colors', ColorViewSet, basename='color')
router.register('measure-units', MeasureUnitViewSet, basename='measure-units')
router.register('categories', CategoryViewSet, basename='category')
router.register('subcategories', SubCategoryViewSet, basename='subcategory')

urlpatterns = [
    path('', include(router.urls)),
]