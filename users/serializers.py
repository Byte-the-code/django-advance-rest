from rest_framework import serializers
from users.models import User, UserProfile, UserDocumentation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserDocumentationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocumentation
        fields = ['document_type', 'document_identifier', 'front_image', 'back_image']

class UserDocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocumentation
        fields = '__all__'

class UserDocumentationListSerializer(serializers.ModelSerializer):
    user_full_name = serializers.CharField(source='user.get_full_name')
    class Meta:
        model = UserDocumentation
        fields = ['id', 'user_full_name', 'document_type', 'document_identifier', 'front_image', 'back_image']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'user_type', 'is_active']

class SellerListSerializer(serializers.ModelSerializer):
    # products_count = serializers.SerializerMethodField()
    document_status = serializers.CharField(source = 'documentation.status')
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'document_status', 'date_joined']
        # fields = ['id', 'first_name', 'last_name', 'email', 'products_count', 'date_joined']


    # def get_products_count(self, obj):
    #     return obj.products.count()