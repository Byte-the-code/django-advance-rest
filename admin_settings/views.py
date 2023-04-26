from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response 
from rest_framework import status

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView,\
    DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from admin_settings.serializers import SubCategorySerializer, ColorSerializer, \
    MeasureUnitSerializer, CategorySerializer
from admin_settings.models import Color, Category, SubCategory, MeasureUnit
from admin_settings.permissions import IsAdminOrReadOnly

# Colors (generic views by separate)
class ColorListAPIView(ListAPIView):

    def get_queryset(self):
        return Color.objects.all()

    def get_serializer_class(self):
        return ColorSerializer

class ColorCreateAPIView(CreateAPIView):
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser]

class ColorRetrieveAPIView(RetrieveAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class ColorUpdateAPIView(UpdateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser]

class ColorDestroyAPIView(DestroyAPIView):
    queryset = Color.objects.all()
    permission_classes = [IsAdminUser]

# Measure units (generic views mixed)
class MeasureUnitListCreateAPIView(ListCreateAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAdminOrReadOnly]

class MeasureUnitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAdminOrReadOnly]


# Categories (generic views mixed)
class CategoryListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# Sub Categories (generic views mixed)
class SubCategoryListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        if not 'category' in self.request.query_params:
            return SubCategory.objects.all()
        return SubCategory.objects.filter(category__id=self.request.query_params['category'])

class SubCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
