from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response 
from rest_framework import status

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView,\
    DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView

from admin_settings.serializers import DefinedConfigurations, SubCategorySerializer, \
    ColorSerializer, MeasureUnitSerializer
from admin_settings.models import Color, Category, SubCategory, MeasureUnit
from admin_settings.permissions import IsAdminOrReadOnly

class ColorListAPIView(ListAPIView):

    def get_queryset(self):
        return Color.objects.all()

    def get_serializer_class(self):
        return DefinedConfigurations

class ColorCreateApiView(CreateAPIView):
    serializer_class = ColorSerializer
    permission_classes = [IsAdminUser]

class ColorRetrieveApiView(RetrieveAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class ColorUpdateApiView(UpdateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class ColorDestroyApiView(DestroyAPIView):
    queryset = Color.objects.all()


class MeasureUnitListCreateApiView(ListCreateAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAdminOrReadOnly]


class MeasureUnitRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsAdminOrReadOnly]











class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = DefinedConfigurations

class SubCategoryListApiView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        if 'category_id' in self.request.query_params:
            return SubCategory.objects.filter(category = self.request.query_params['category_id'])
        return SubCategory.objects.all()
