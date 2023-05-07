from rest_framework import viewsets

from admin_settings.serializers import SubCategorySerializer, ColorSerializer, \
    MeasureUnitSerializer, CategorySerializer
from admin_settings.models import Color, Category, SubCategory, MeasureUnit
from admin_settings.permissions import IsAdminOrReadOnly

class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = (IsAdminOrReadOnly,)

class MeasureUnitViewSet(viewsets.ModelViewSet):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = (IsAdminOrReadOnly,)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if not 'category' in self.request.query_params:
            return SubCategory.objects.all()
        return SubCategory.objects.filter(category__id=self.request.query_params['category'])
