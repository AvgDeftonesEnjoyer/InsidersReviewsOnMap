from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Location, Review, ReviewLike

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


class LocationSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Location.CATEGORY_CHOICES)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Location
        fields = ['id', 'title', 'description', 'category', 'average_rating', 'created_at', 'updated_at']
        
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'location', 'text', 'rating', 'created_at']
        
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