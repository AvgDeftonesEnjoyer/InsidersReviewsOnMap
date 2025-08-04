import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LocationSerializer, ReviewSerializer, ReviewLikeSerializer
from .models import Location, Review, ReviewLike
from .filters import LocationFilter


User = get_user_model()

# Це кешований список без фільтрації. Якщо потрібен фільтр — використовуйте /locations/
class CachedLocationListView(APIView):
    def get(self, request):
        cached_data = cache.get('location_list')
        if cached_data:
            return Response(cached_data)
        
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many = True)
        cache.set('location_list', serializer.data, timeout=60*5)
        return Response(serializer.data)

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({'message' : 'User Created'}, status=201)
        return Response(serializer.errors, status = 400)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return Response({'message' : 'Login successful'})
        return Response({'error': 'Invalid credentials'}, status = 401)

class LogOutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out'})
            
class LocationListCreateView(generics.ListCreateAPIView):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = LocationFilter  
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        return Location.objects.filter(is_active = True).annotate(
            average_rating = Avg('reviews__rating')
        )
    
class LocationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class ReviewLikeCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        review_id = request.data.get('review_id')
        is_like = request.data.get('is_like')
        
        if review_id is None or is_like is None:
            return Response({'error': 'review_id and is_like are required'}, status=400)
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=404)
        like_obj, created = ReviewLike.objects.update_or_create(
            user=user,
            review=review,
            defaults={'is_like' : is_like}
        )
        
        return Response({
            'message': 'Like Updated' if not created else 'Like created',
            'is_like' : like_obj.is_like
        }, status = 200)


class LocationExportView(APIView):    
    def get(self, request):
        format = request.GET.get('format', 'json')
        
        locations = Location.objects.all().values(
            'id', 'title', 'description', 'category', 'created_at', 'updated_at'
        )
        df = pd.DataFrame(list(locations))
        
        if format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="locations.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response
        
        elif format == 'json':
            return Response(df.to_dict(orient='records'))

        return Response({'error': 'Invalid format'}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    obj, created = ReviewLike.objects.get_or_create(user=request.user, review=review)

    if not created and obj.is_like:
        obj.delete()
        return Response({"message": "Like removed"})
    
    obj.is_like = True
    obj.save()
    return Response({"message": "Liked"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    obj, created = ReviewLike.objects.get_or_create(user=request.user, review=review)

    if not created and not obj.is_like:
        obj.delete()
        return Response({"message": "Dislike removed"})
    
    obj.is_like = False
    obj.save()
    return Response({"message": "Disliked"})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_location_active(request, pk):
    try:
        location = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return Response({'error': 'Location not found'}, status=404)
    
    location.is_active = not location.is_active
    location.save()
    return Response({'message': f'is_active set to {location.is_active}'}, status=200)

# Create your views here.
