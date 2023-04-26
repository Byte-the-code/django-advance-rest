from rest_framework import serializers

from admin_settings.models import SubCategory, Category, Color, MeasureUnit

class DefinedConfigurations(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=70)

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        category = Category.objects.get(id = data['category'])
        data['category'] = DefinedConfigurations(category).data
        return data