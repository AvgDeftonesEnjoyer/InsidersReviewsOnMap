from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator as Min, MaxValueValidator as Max

User = get_user_model()   

class Location(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('park', 'Park'),
        ('shop', 'Shop'),
        ('museum', 'Museum'),
    ]
    
    title = models.CharField(max_length = 200)
    description = models.TextField(blank = True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default = True)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    location = models.ForeignKey(Location, on_delete = models.CASCADE, related_name = 'reviews')
    text = models.TextField(help_text = 'Write your review here')
    rating = models.IntegerField(
        validators = [Min(1), Max(5)],
        help_text = 'Rating must be beetween 1 and 5'
    )
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'Review by {self.user.username} for {self.location.title} ({self.rating}/5)'

class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    review = models.ForeignKey(Review, on_delete = models.CASCADE, related_name = 'likes')
    is_like = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        unique_together = ('user', 'review')
        
    def __str__(self):
        state = '👍' if self.is_like else '👎'
        return f'{state} by {self.user.username} for review {self.review}'
            
# Create your models here.
