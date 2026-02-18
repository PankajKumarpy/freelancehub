from django.urls import path
from . import views

urlpatterns = [
    # Home & Auth
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Profile
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile_view_user'),
    
    # Gigs
    path('gigs/', views.GigListView.as_view(), name='gig_list'),
    path('gigs/<int:pk>/', views.GigDetailView.as_view(), name='gig_detail'),
    path('gigs/create/', views.GigCreateView.as_view(), name='gig_create'),
    path('gigs/<int:pk>/edit/', views.GigUpdateView.as_view(), name='gig_edit'),
    path('gigs/<int:pk>/delete/', views.GigDeleteView.as_view(), name='gig_delete'),
    path('gigs/<int:gig_id>/purchase/', views.purchase_gig, name='purchase_gig'),
    
    # Jobs
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    
    # Bids
    path('jobs/<int:job_id>/bid/', views.submit_bid, name='submit_bid'),
    path('bids/<int:bid_id>/accept/', views.accept_bid, name='accept_bid'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/complete/', views.complete_order, name='complete_order'),
    
    # Reviews
    path('reviews/submit/<int:order_id>/', views.submit_review, name='submit_review'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    
    # Messages
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:user_id>/', views.conversation, name='conversation'),
    path('messages/send/<int:user_id>/', views.send_message, name='send_message'),
]
