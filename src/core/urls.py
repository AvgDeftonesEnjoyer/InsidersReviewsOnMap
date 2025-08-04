from django.urls import path
from .views import (RegisterView, LoginView, LogOutView, LocationListCreateView, 
                    LocationRetrieveUpdateDestroyView, ReviewListCreateView, 
                    CachedLocationListView, ReviewLikeCreateView, LocationExportView, 
                    toggle_location_active, like_review, dislike_review)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('locations/', LocationListCreateView.as_view(), name='location-list-create'),
    path('locations/<int:pk>/', LocationRetrieveUpdateDestroyView.as_view(), name='location-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('cached-locations/', CachedLocationListView.as_view(), name='cached-location-list'),   
    path('review-likes/', ReviewLikeCreateView.as_view(), name='review-like-create'),
    path('locations/export/', LocationExportView.as_view(), name='location-export'),
    path('locations/<int:pk>/toggle_active/', toggle_location_active, name='toggle-location-active'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/reviews/<int:pk>/like/', like_review, name='review-like'),
    path('api/reviews/<int:pk>/dislike/', dislike_review, name='review-dislike'),
]
