from django.urls import path, include
from rest_framework.routers import DefaultRouter

from products.views import ProductsViewSet, MyproductsViewSet

router = DefaultRouter()
router.register('all-products', ProductsViewSet, basename='products-view-set')
router.register('my-products', MyproductsViewSet, basename='my-products' )


urlpatterns = [
    path('', include(router.urls)),
]
