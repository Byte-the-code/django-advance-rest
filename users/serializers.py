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

