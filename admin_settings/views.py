from rest_framework.generics import ListAPIView

from admin_settings.serializers import DefinedConfigurations, SubCategorySerializer
from admin_settings.models import Color, Category, SubCategory, MeasureUnit

class ColorListAPIView(ListAPIView):

    def get_queryset(self):
        return Color.objects.all()

    def get_serializer_class(self):
        return DefinedConfigurations

class MeasureUnitApiView(ListAPIView):
    queryset = MeasureUnit.objects.all()
    serializer_class = DefinedConfigurations

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = DefinedConfigurations

class SubCategoryListApiView(ListAPIView):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        if 'category_id' in self.request.query_params:
            return SubCategory.objects.filter(category = self.request.query_params['category_id'])
        return SubCategory.objects.all()
