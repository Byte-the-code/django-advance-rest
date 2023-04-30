from rest_framework import serializers

from users.models import User
from products.models import Product, ExtraImage
from admin_settings.serializers import CategorySerializer, SubCategorySerializer, MeasureUnitSerializer, ColorSerializer

class SellerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class ExtraProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraImage
        fields = ['pk', 'image']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data if instance.category else '-'
        data['subcategory'] = SubCategorySerializer(instance.subcategory).data if instance.subcategory else '-'
        data['measure_unit'] =MeasureUnitSerializer(instance.measure_unit).data if instance.measure_unit else '-'
        data['color'] = ColorSerializer(instance.color).data  if instance.color else '-'
        data['owner'] = SellerNameSerializer(instance.owner).data
        data['extra_images'] = ExtraProductsImageSerializer(instance.extra_images.all(), many=True).data
        return data

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['is_deleted', 'is_distinguished', 'is_admin_banned']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'price', 'image_1', 'creation_date']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data if instance.category else '-'
        data['subcategory'] = SubCategorySerializer(instance.subcategory).data if instance.subcategory else '-'
        data['measure_unit'] =MeasureUnitSerializer(instance.measure_unit).data if instance.measure_unit else '-'
        data['color'] = ColorSerializer(instance.color).data  if instance.color else '-'
        data['owner'] = SellerNameSerializer(instance.owner).data
        return data