import mercadopago

from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db.models import Value
from django.shortcuts import get_object_or_404
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from django.http import HttpResponse

from admin_settings.models import SubCategory
from products.permissions import IsSeller, IsSellerOrReadOnly, IsOwner
from products.serializers import ProductListSerializer, ProductSerializer, ProductCreateSerializer
from products.models import Product, Order

from django_base.settings import MERCADOPAGO_TOKEN
from products.tasks import load_products

class MyproductsViewSet(ModelViewSet):

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsSeller]
        else:
            return []

    def get_queryset(self):
        products = self.request.user.products.filter().order_by('id')

        if 'search' in self.request.query_params:
            products = products.filter(name__icontains = self.request.query_params['search'])

        if 'category' in self.request.query_params:
            products = products.filter(category = self.request.query_params['category'])

        if 'subcategory' in self.request.query_params:
            products = products.filter(subcategory = self.request.query_params['subcategory'])

        if 'color' in self.request.query_params:
            products = products.filter(color = self.request.query_params['color'])

        if 'measure_unit' in self.request.query_params:
            products = products.filter(measure_unit = self.request.query_params['measure_unit'])
            
        order_by = self.request.query_params.get('order_by', 'id')
        return products.order_by(order_by)

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'create':
            return ProductCreateSerializer
        else:
            return ProductSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['patch'], url_path='mark-distinguished')
    def mark_distinguished(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_distinguished:
            return Response('Product is already distinguished', status=status.HTTP_400_BAD_REQUEST)

        if instance.owner.products.filter(is_distinguished=True, is_deleted = False).count() >= 3:
            return Response('You have already distinguished 3 products', status=status.HTTP_400_BAD_REQUEST)

        instance.is_distinguished = True
        instance.save()
        return Response('Product marked as distinguished', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='unmark-distinguished')
    def unmark_distinguished(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_distinguished:
            return Response('Product is not distinguished', status=status.HTTP_400_BAD_REQUEST)

        instance.is_distinguished = False
        instance.save()
        return Response('Product unmarked as distinguished', status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='upload-product-massive', permission_classes=[IsSeller])
    def upload_product_massive(self, request, *args, **kwargs):
        load_products.delay(request.user.pk)
        return Response('Products are being loaded', status=status.HTTP_200_OK)


class ProductsViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProductListSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            products = Product.objects.filter(
                        owner__documentation__status='approved',
                        is_deleted=False,).order_by('id')
        else:
            products = Product.objects.filter(
                        owner__documentation__status='approved',
                        is_deleted=False,
                        is_admin_banned=False).order_by('id')

        if 'search' in self.request.query_params:
            products = (products.annotate(search_field = 
                            Concat('name', Value(' '), 
                            'owner__first_name', Value(' '), 
                            'owner__last_name'))
                            .filter(search_field__icontains = self.request.query_params['search']))

        if 'category' in self.request.query_params:
            products = products.filter(category = self.request.query_params['category'])

        if 'subcategory' in self.request.query_params:
            products = products.filter(subcategory = self.request.query_params['subcategory'])

        if 'color' in self.request.query_params:
            products = products.filter(color = self.request.query_params['color'])

        if 'measure_unit' in self.request.query_params:
            products = products.filter(measure_unit = self.request.query_params['measure_unit'])

        order_by = self.request.query_params.get('order_by', 'id')
        products = products.order_by(order_by)

        return products

    @action(detail=True, methods=['patch'], url_path='ban-product', permission_classes=[IsAdminUser])
    def ban_product(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_admin_banned = True
        instance.save()
        return Response('Product banned', status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='unban-product', permission_classes=[IsAdminUser])
    def unban_product(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_admin_banned = False
        instance.save()
        return Response('Product unbanned', status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='buy-product')
    def buy_product(self, request, *args, **kwargs):
        products = request.data.get('products', None)

        items = []
        products_ids = []

        if not products:
            return Response('No products provided', status=status.HTTP_400_BAD_REQUEST)
        for product in products:
            try:
                product_to_buy = Product.objects.get(pk=product['pk'])
            except Product.DoesNotExist:
                return Response('Product does not exist', status=status.HTTP_400_BAD_REQUEST)
            products_ids.append(product_to_buy.pk)
            items.append({
                "title": product_to_buy.name,
                "quantity": product['quantity'],
                "unit_price": product_to_buy.price,
            })
        
        new_order = Order.objects.create(buyer=request.user)
        new_order.products.set(products_ids)

        sdk = mercadopago.SDK(MERCADOPAGO_TOKEN)
        preference_data = {
            'external_reference': new_order.pk,
            "items": items,
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        link = preference.get('init_point', None)

        new_order.mercado_link = link
        new_order.save()

        return Response(link, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], url_path='mercado-pay-notification', permission_classes=[AllowAny])
    def mercado_pay_notification(self, request, *args, **kwargs):
        sdk = mercadopago.SDK(MERCADOPAGO_TOKEN)
        payment_id = request.data['data'].get('id')
        if not payment_id:
            return Response('No payment id provided', status=status.HTTP_400_BAD_REQUEST)
        payment_info = sdk.payment().get(payment_id)
        payment_info = payment_info['response']
        if payment_info['status'] == 'approved':
            external_reference = payment_info['external_reference']
            order = Order.objects.get(pk=external_reference)
            order.is_paid = True
            order.save()
            return Response('Payment approved', status=status.HTTP_200_OK)
        return Response('Payment not approved', status=status.HTTP_400_BAD_REQUEST)