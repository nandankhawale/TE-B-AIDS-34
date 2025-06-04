from django.db import models
from django.utils import timezone

class NumberEntry(models.Model):
    CATEGORY_CHOICES = [
        ('p', 'Prime'),
        ('f', 'Fibonacci'),
        ('e', 'Even'),
        ('r', 'Random'),
    ]
    
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    number = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['category', 'number']
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_category_display()}: {self.number}"

class AuthToken(models.Model):
    access_token = models.TextField()
    token_type = models.CharField(max_length=50, default='Bearer')
    expires_in = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    
    @property
    def is_expired(self):
        import time
        return time.time() >= self.expires_in
    
    def __str__(self):
        return f"Token expires at {self.expires_in}"