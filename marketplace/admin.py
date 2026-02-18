from django.contrib import admin
from .models import FreelancerProfile, ClientProfile, Category, Gig, Job, Bid, Order, Message, Review


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'experience', 'hourly_rate', 'rating', 'total_earnings', 'created_at']
    list_filter = ['experience', 'rating', 'created_at']
    search_fields = ['user__username', 'user__email', 'skills', 'bio']
    readonly_fields = ['created_at', 'rating', 'total_earnings']


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'contact_info', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email', 'company_name']
    readonly_fields = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ['title', 'freelancer', 'category', 'price', 'delivery_time', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    search_fields = ['title', 'description', 'freelancer__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'category', 'budget', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'client__username']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['job', 'freelancer', 'bid_amount', 'delivery_days', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['job__title', 'freelancer__username', 'proposal_text']
    readonly_fields = ['created_at']
    list_editable = ['status']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'freelancer', 'price', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['client__username', 'freelancer__username']
    readonly_fields = ['created_at']
    list_editable = ['status']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp']
    search_fields = ['sender__username', 'receiver__username', 'content']
    readonly_fields = ['timestamp']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['order', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['review_text', 'order__client__username', 'order__freelancer__username']
    readonly_fields = ['created_at']
