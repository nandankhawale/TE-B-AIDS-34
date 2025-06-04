from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import NumberEntry, AuthToken

@admin.register(NumberEntry)
class NumberEntryAdmin(admin.ModelAdmin):
    list_display = ['category', 'number', 'timestamp']
    list_filter = ['category', 'timestamp']
    ordering = ['-timestamp']

@admin.register(AuthToken)
class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ['token_type', 'expires_in', 'created_at', 'is_expired']
    readonly_fields = ['is_expired']