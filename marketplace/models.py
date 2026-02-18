from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class FreelancerProfile(models.Model):
    """Profile for freelancers offering services"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.TextField(help_text="Comma-separated skills")
    bio = models.TextField(max_length=1000)
    experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Freelancer"
    
    def update_rating(self):
        """Update freelancer rating based on reviews"""
        from django.db.models import Avg
        avg_rating = Review.objects.filter(order__freelancer=self.user).aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            self.rating = round(avg_rating, 2)
            self.save()


class ClientProfile(models.Model):
    """Profile for clients hiring freelancers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True)
    contact_info = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Client"
    
    def total_spent(self):
        """Calculate total amount spent by client"""
        return Order.objects.filter(client=self.user, status='Completed').aggregate(
            total=models.Sum('price'))['total'] or 0


class Category(models.Model):
    """Categories for gigs and jobs"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Gig(models.Model):
    """Services offered by freelancers"""
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gigs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='gigs')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    delivery_time = models.PositiveIntegerField(help_text="Delivery time in days")
    image = models.ImageField(upload_to='gigs/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Job(models.Model):
    """Jobs posted by clients"""
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    deadline = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='jobs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def has_accepted_bid(self):
        """Check if job has an accepted bid"""
        return self.bids.filter(status='Accepted').exists()


class Bid(models.Model):
    """Freelancer proposals on jobs"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='bids')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    proposal_text = models.TextField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    delivery_days = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['job', 'freelancer']  # Prevent duplicate bids
    
    def __str__(self):
        return f"Bid by {self.freelancer.username} on {self.job.title}"


class Order(models.Model):
    """Orders created when gig purchased or bid accepted"""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_orders')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_orders')
    gig = models.ForeignKey(Gig, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.gig:
            return f"Order for Gig: {self.gig.title}"
        elif self.job:
            return f"Order for Job: {self.job.title}"
        return f"Order #{self.id}"


class Message(models.Model):
    """Messages between users"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class Review(models.Model):
    """Reviews and ratings for completed orders"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for Order #{self.order.id} - {self.rating} stars"
