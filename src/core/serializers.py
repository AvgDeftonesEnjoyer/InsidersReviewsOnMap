from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, Location, Review, ReviewLike

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class LocationSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = Location
        fields = ['id', 'title', 'description', 'category', 'category_id', 'created_at', 'updated_at']
        
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='location',
        write_only=True
    )
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'location_id', 'text', 'rating', 'created_at']
        
class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    review_id = serializers.PrimaryKeyRelatedField(
        queryset = Review.objects.all(),
        source = 'review',
        write_only = True
    )
    
    class Meta:
        model = ReviewLike
        fields = ['id', 'user', 'review_id', 'is_like', 'created_at']