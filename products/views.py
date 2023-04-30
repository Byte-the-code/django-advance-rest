from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db.models import Value
from django.shortcuts import get_object_or_404
from django.db.models.functions import Concat
from django.core.paginator import Paginator

from admin_settings.models import SubCategory
from products.permissions import IsSeller, IsSellerOrReadOnly
from products.serializers import ProductListSerializer, ProductSerializer
from products.models import Product


# Products
class MyProductsView(APIView):
    permission_classes = [IsSeller, ]

    def get(self, request):
        products = request.user.products.filter(is_deleted=False).order_by('id')

        if 'search' in request.query_params:
            products = products.filter(name__icontains = request.query_params['search'])

        if 'category' in request.query_params:
            products = products.filter(category = request.query_params['category'])

        if 'subcategory' in request.query_params:
            products = products.filter(subcategory = request.query_params['subcategory'])

        if 'color' in request.query_params:
            products = products.filter(color = request.query_params['color'])

        if 'measure_unit' in request.query_params:
            products = products.filter(measure_unit = request.query_params['measure_unit'])
        order_by = request.query_params.get('order_by', 'id')
        products = products.order_by(order_by)

        per_page = request.query_params.get('per_page', 5)
        page = request.query_params.get('page', 1)
        paginator = Paginator(products, per_page)
        data = paginator.page(page)

        serializer = ProductListSerializer(data, many=True)


        return Response({'page':page, 'total_pages':paginator.num_pages, 
                    'total_items':products.count(), 'data':serializer.data},
                    status=status.HTTP_200_OK)

    def post(self, request):

        if 'category' in request.data and 'subcategory' in request.data:
            if not SubCategory.objects.filter(id=request.data['subcategory'], category__id=request.data['category']).exists():
                return Response({'error': 'That subcategory does not belong to the given category'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['owner'] = request.user.pk
        data['is_deleted'] = False
        data['is_admin_banned'] = False
        data['is_distinguished'] = False

        serializer = ProductSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProductsRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsSellerOrReadOnly]

    def get(self, request, pk):
        product = get_object_or_404(Product, pk = pk, is_deleted=False)
        if not (request.user.is_authenticated and request.user == product.owner):

            if product.is_admin_banned:
                return Response({'error':'This product is banned by an admin'}, status=status.HTTP_400_BAD_REQUEST)

            if product.owner.documentation.status != 'Approved':
                return Response({'error':'The seller does not have documents approved'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProductSerializer(product)

        return Response({'data':serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk = pk, is_deleted=False)
        if not (request.user.is_authenticated and request.user == product.owner):
            return Response({'error':'You are not the owner of this product'}, status=status.HTTP_400_BAD_REQUEST)

        if 'category' in request.data and 'subcategory' in request.data:
            if not SubCategory.objects.filter(id=request.data['subcategory'], category__id=request.data['category']).exists():
                return Response({'error': 'That subcategory does not belong to the given category'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['owner'] = product.owner.pk
        data['is_deleted'] = product.is_deleted
        data['is_admin_banned'] = product.is_admin_banned
        data['is_distinguished'] = product.is_distinguished

        serializer = ProductSerializer(product, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)

        return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk = pk, is_deleted=False)
        if not (request.user.is_authenticated and request.user == product.owner):
            return Response({'error':'You are not the owner of this product'}, status=status.HTTP_400_BAD_REQUEST)

        product.is_deleted = True
        product.save()

        return Response({'data':'Product deleted successfully'}, status=status.HTTP_200_OK)

class ProductDistinguisehedView(APIView):
    permission_classes = [IsSeller]
    def patch(self, request, pk):

        product = get_object_or_404(Product, pk = pk, is_deleted=False)
        if request.user != product.owner:
            return Response({'error':'You are not the owner of this product'}, status=status.HTTP_400_BAD_REQUEST)
        
        if 'is_distinguished' not in request.data:
            return Response({'error': 'is_distinguished is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_distinguished = request.data['is_distinguished'].lower() == 'true'
        if is_distinguished: # if is_distinguished is true
            if product.is_distinguished:
                return Response({'error': 'This product is already distinguished'}, status=status.HTTP_400_BAD_REQUEST)
            if product.owner.products.filter(is_distinguished=True).count() >= 3:
                return Response({'error': 'You have already distinguished 3 products'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not product.is_distinguished:
                return Response({'error': 'This product is not distinguished'}, status=status.HTTP_400_BAD_REQUEST)

        product.is_distinguished = is_distinguished
        product.save()
        return Response({'data': f'The product distinguished state is {product.is_distinguished}'}, status=status.HTTP_200_OK)

class ProductsListView(APIView):
    permission_classes = []

    def get(self, request):
        products = Product.objects.filter(
                    owner__documentation__status='approved',
                    is_deleted=False,
                    is_admin_banned=False).order_by('id')

        if 'search' in request.query_params:
            products = (products.annotate(search_field = 
                            Concat('name', Value(' '), 
                            'owner__first_name', Value(' '), 
                            'owner__last_name'))
                            .filter(search_field__icontains = request.query_params['search']))

        if 'category' in request.query_params:
            products = products.filter(category = request.query_params['category'])

        if 'subcategory' in request.query_params:
            products = products.filter(subcategory = request.query_params['subcategory'])

        if 'color' in request.query_params:
            products = products.filter(color = request.query_params['color'])

        if 'measure_unit' in request.query_params:
            products = products.filter(measure_unit = request.query_params['measure_unit'])

        order_by = request.query_params.get('order_by', 'id')
        products = products.order_by(order_by)

        per_page = request.query_params.get('per_page', 5)
        page = request.query_params.get('page', 1)
        paginator = Paginator(products, per_page)
        data = paginator.page(page)

        serializer = ProductListSerializer(data, many=True)


        return Response({'page':page, 'total_pages':paginator.num_pages, 
                    'total_items':products.count(), 'data':serializer.data},
                    status=status.HTTP_200_OK)

class BanProductsAdminView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        if not 'is_admin_banned' in request.data:
            return Response({'error':'is_admin_banned field is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, pk = pk, is_deleted=False)
        product.is_admin_banned = request.data['is_admin_banned']
        product.save()

        return Response({'data':f"The product banned state is {request.data['is_admin_banned']}"}, status=status.HTTP_200_OK)