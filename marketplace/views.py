from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.views.decorators.cache import never_cache
from .models import (
    FreelancerProfile, ClientProfile, Category, Gig, Job, 
    Bid, Order, Message, Review
)
from .forms import (
    UserRegistrationForm, FreelancerProfileForm, ClientProfileForm,
    GigForm, JobForm, BidForm, MessageForm, ReviewForm
)


# ==================== Home & Authentication ====================

def home(request):
    """Home page with featured gigs"""
    featured_gigs = Gig.objects.filter(is_active=True).order_by('-created_at')[:8]
    categories = Category.objects.all()[:6]
    context = {
        'featured_gigs': featured_gigs,
        'categories': categories,
    }
    return render(request, 'marketplace/home.html', context)


def register(request):
    """User registration with role selection"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            
            # Create profile based on role
            if role == 'freelancer':
                FreelancerProfile.objects.create(
                    user=user,
                    skills='',
                    bio='',
                    hourly_rate=0
                )
            else:
                ClientProfile.objects.create(
                    user=user,
                    contact_info=user.email
                )
            
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Please complete your profile.')
            return redirect('profile_edit')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'marketplace/auth/register.html', {'form': form})


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'marketplace/auth/login.html')



@never_cache
def user_logout(request):
    """User logout - clears session and prevents browser caching"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    response = redirect('home')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response



# ==================== Profile Views ====================

@login_required
def profile_view(request, username=None):
    """View user profile"""
    if username:
        from django.contrib.auth.models import User
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    freelancer_profile = FreelancerProfile.objects.filter(user=user).first()
    client_profile = ClientProfile.objects.filter(user=user).first()
    
    context = {
        'profile_user': user,
        'freelancer_profile': freelancer_profile,
        'client_profile': client_profile,
    }
    
    if freelancer_profile:
        context['gigs'] = Gig.objects.filter(freelancer=user, is_active=True)
        context['reviews'] = Review.objects.filter(order__freelancer=user)
    
    return render(request, 'marketplace/profile/profile.html', context)


@login_required
def profile_edit(request):
    """Edit user profile"""
    freelancer_profile = FreelancerProfile.objects.filter(user=request.user).first()
    client_profile = ClientProfile.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        if freelancer_profile:
            form = FreelancerProfileForm(request.POST, request.FILES, instance=freelancer_profile)
        else:
            form = ClientProfileForm(request.POST, request.FILES, instance=client_profile)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_view')
    else:
        if freelancer_profile:
            form = FreelancerProfileForm(instance=freelancer_profile)
        else:
            form = ClientProfileForm(instance=client_profile)
    
    return render(request, 'marketplace/profile/profile_edit.html', {'form': form})


# ==================== Gig Views ====================

class GigListView(ListView):
    """List all active gigs"""
    model = Gig
    template_name = 'marketplace/gigs/gig_list.html'
    context_object_name = 'gigs'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Gig.objects.filter(is_active=True)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(freelancer__freelancer_profile__skills__icontains=search)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by price
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class GigDetailView(DetailView):
    """View gig details"""
    model = Gig
    template_name = 'marketplace/gigs/gig_detail.html'
    context_object_name = 'gig'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gig = self.get_object()
        context['freelancer_profile'] = FreelancerProfile.objects.filter(user=gig.freelancer).first()
        context['reviews'] = Review.objects.filter(order__gig=gig)
        return context


class GigCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new gig (freelancers only)"""
    model = Gig
    form_class = GigForm
    template_name = 'marketplace/gigs/gig_form.html'
    success_url = reverse_lazy('gig_list')
    
    def test_func(self):
        # Only freelancers can create gigs
        return FreelancerProfile.objects.filter(user=self.request.user).exists()
    
    def form_valid(self, form):
        form.instance.freelancer = self.request.user
        messages.success(self.request, 'Gig created successfully!')
        return super().form_valid(form)


class GigUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update gig (owner only)"""
    model = Gig
    form_class = GigForm
    template_name = 'marketplace/gigs/gig_form.html'
    success_url = reverse_lazy('gig_list')
    
    def test_func(self):
        gig = self.get_object()
        return gig.freelancer == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Gig updated successfully!')
        return super().form_valid(form)


class GigDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete gig (owner only)"""
    model = Gig
    template_name = 'marketplace/gigs/gig_confirm_delete.html'
    success_url = reverse_lazy('gig_list')
    
    def test_func(self):
        gig = self.get_object()
        return gig.freelancer == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Gig deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==================== Job Views ====================

class JobListView(ListView):
    """List all jobs"""
    model = Job
    template_name = 'marketplace/jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Job.objects.all()
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            )
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class JobDetailView(DetailView):
    """View job details"""
    model = Job
    template_name = 'marketplace/jobs/job_detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        context['bids'] = job.bids.all()
        context['bid_form'] = BidForm()
        
        # Check if user already bid
        if self.request.user.is_authenticated:
            context['user_bid'] = Bid.objects.filter(
                job=job, 
                freelancer=self.request.user
            ).first()
        
        return context


class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Post a new job (clients only)"""
    model = Job
    form_class = JobForm
    template_name = 'marketplace/jobs/job_form.html'
    success_url = reverse_lazy('job_list')
    
    def test_func(self):
        # Only clients can post jobs
        return ClientProfile.objects.filter(user=self.request.user).exists()
    
    def form_valid(self, form):
        form.instance.client = self.request.user
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)


# ==================== Bid Views ====================

@login_required
def submit_bid(request, job_id):
    """Submit a bid on a job"""
    job = get_object_or_404(Job, id=job_id)
    
    # Check if user is a freelancer
    if not FreelancerProfile.objects.filter(user=request.user).exists():
        messages.error(request, 'Only freelancers can submit bids.')
        return redirect('job_detail', pk=job_id)
    
    # Check if job is open
    if job.status != 'Open':
        messages.error(request, 'This job is no longer accepting bids.')
        return redirect('job_detail', pk=job_id)
    
    # Check if already bid
    if Bid.objects.filter(job=job, freelancer=request.user).exists():
        messages.error(request, 'You have already submitted a bid for this job.')
        return redirect('job_detail', pk=job_id)
    
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.job = job
            bid.freelancer = request.user
            bid.save()
            messages.success(request, 'Bid submitted successfully!')
            return redirect('job_detail', pk=job_id)
    
    return redirect('job_detail', pk=job_id)


@login_required
def accept_bid(request, bid_id):
    """Accept a bid (job owner only)"""
    bid = get_object_or_404(Bid, id=bid_id)
    job = bid.job
    
    # Check if user is job owner
    if job.client != request.user:
        return HttpResponseForbidden("You don't have permission to accept this bid.")
    
    # Check if job already has accepted bid
    if job.has_accepted_bid():
        messages.error(request, 'This job already has an accepted bid.')
        return redirect('job_detail', pk=job.id)
    
    # Accept bid
    bid.status = 'Accepted'
    bid.save()
    
    # Update job status
    job.status = 'In Progress'
    job.save()
    
    # Create order
    Order.objects.create(
        client=job.client,
        freelancer=bid.freelancer,
        job=job,
        price=bid.bid_amount,
        status='In Progress'
    )
    
    # Reject other bids
    job.bids.exclude(id=bid_id).update(status='Rejected')
    
    messages.success(request, 'Bid accepted! Order created.')
    return redirect('order_list')


# ==================== Order Views ====================

@login_required
def order_list(request):
    """List user's orders"""
    freelancer_profile = FreelancerProfile.objects.filter(user=request.user).first()
    
    if freelancer_profile:
        orders = Order.objects.filter(freelancer=request.user)
    else:
        orders = Order.objects.filter(client=request.user)
    
    context = {
        'orders': orders.order_by('-created_at'),
    }
    return render(request, 'marketplace/orders/order_list.html', context)


@login_required
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user is part of the order
    if order.client != request.user and order.freelancer != request.user:
        return HttpResponseForbidden("You don't have permission to view this order.")
    
    context = {
        'order': order,
        'review': Review.objects.filter(order=order).first(),
    }
    return render(request, 'marketplace/orders/order_detail.html', context)


@login_required
def purchase_gig(request, gig_id):
    """Purchase a gig"""
    gig = get_object_or_404(Gig, id=gig_id)
    
    # Check if user is a client
    if not ClientProfile.objects.filter(user=request.user).exists():
        messages.error(request, 'Only clients can purchase gigs.')
        return redirect('gig_detail', pk=gig_id)
    
    # Create order
    order = Order.objects.create(
        client=request.user,
        freelancer=gig.freelancer,
        gig=gig,
        price=gig.price,
        status='In Progress'
    )
    
    messages.success(request, 'Gig purchased successfully! Order created.')
    return redirect('order_detail', order_id=order.id)


@login_required
def complete_order(request, order_id):
    """Mark order as complete (client only)"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user is client
    if order.client != request.user:
        return HttpResponseForbidden("Only the client can complete the order.")
    
    order.status = 'Completed'
    order.completed_at = timezone.now()
    order.save()
    
    # Update job status if applicable
    if order.job:
        order.job.status = 'Completed'
        order.job.save()
    
    messages.success(request, 'Order marked as complete! You can now leave a review.')
    return redirect('order_detail', order_id=order_id)


# ==================== Review Views ====================

@login_required
def submit_review(request, order_id):
    """Submit a review for completed order"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user is client
    if order.client != request.user:
        return HttpResponseForbidden("Only the client can review the order.")
    
    # Check if order is completed
    if order.status != 'Completed':
        messages.error(request, 'You can only review completed orders.')
        return redirect('order_detail', order_id=order_id)
    
    # Check if review already exists
    if Review.objects.filter(order=order).exists():
        messages.error(request, 'You have already reviewed this order.')
        return redirect('order_detail', order_id=order_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('order_detail', order_id=order_id)
    else:
        form = ReviewForm()
    
    return render(request, 'marketplace/orders/submit_review.html', {'form': form, 'order': order})


# ==================== Dashboard Views ====================

@login_required
def dashboard(request):
    """Unified dashboard - shows content based on user role"""
    freelancer_profile = FreelancerProfile.objects.filter(user=request.user).first()
    client_profile = ClientProfile.objects.filter(user=request.user).first()

    if freelancer_profile:
        # Freelancer dashboard data
        total_earnings = freelancer_profile.total_earnings
        active_orders = Order.objects.filter(freelancer=request.user, status='In Progress').count()
        completed_orders = Order.objects.filter(freelancer=request.user, status='Completed').count()
        total_gigs = Gig.objects.filter(freelancer=request.user, is_active=True).count()
        recent_orders = Order.objects.filter(freelancer=request.user).order_by('-created_at')[:5]
        pending_bids = Bid.objects.filter(freelancer=request.user, status='Pending').order_by('-created_at')[:5]
        context = {
            'freelancer_profile': freelancer_profile,
            'total_earnings': total_earnings,
            'active_orders': active_orders,
            'completed_orders': completed_orders,
            'total_gigs': total_gigs,
            'recent_orders': recent_orders,
            'pending_bids': pending_bids,
        }
        return render(request, 'marketplace/dashboard/freelancer.html', context)

    elif client_profile:
        # Client dashboard data
        total_spent = client_profile.total_spent()
        active_orders = Order.objects.filter(client=request.user, status='In Progress').count()
        completed_orders = Order.objects.filter(client=request.user, status='Completed').count()
        posted_jobs = Job.objects.filter(client=request.user).count()
        recent_orders = Order.objects.filter(client=request.user).order_by('-created_at')[:5]
        recent_jobs = Job.objects.filter(client=request.user).order_by('-created_at')[:5]
        context = {
            'client_profile': client_profile,
            'total_spent': total_spent,
            'active_orders': active_orders,
            'completed_orders': completed_orders,
            'posted_jobs': posted_jobs,
            'recent_orders': recent_orders,
            'recent_jobs': recent_jobs,
        }
        return render(request, 'marketplace/dashboard/client.html', context)

    else:
        # No profile yet - prompt to complete setup
        messages.info(request, 'Please complete your profile to access your dashboard.')
        return redirect('profile_edit')


@login_required
def freelancer_dashboard(request):
    return redirect('dashboard')


@login_required
def client_dashboard(request):
    return redirect('dashboard')




# ==================== Messaging Views ====================

@login_required
def message_list(request):
    """List all conversations"""
    from django.db.models import Q, Max
    from django.contrib.auth.models import User
    
    # Get all users the current user has messaged with
    sent_to = Message.objects.filter(sender=request.user).values_list('receiver', flat=True).distinct()
    received_from = Message.objects.filter(receiver=request.user).values_list('sender', flat=True).distinct()
    
    user_ids = set(list(sent_to) + list(received_from))
    conversations = User.objects.filter(id__in=user_ids)
    
    # Get last message for each conversation
    conversation_data = []
    for user in conversations:
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)
        ).order_by('-timestamp').first()
        
        unread_count = Message.objects.filter(
            sender=user, receiver=request.user, is_read=False
        ).count()
        
        conversation_data.append({
            'user': user,
            'last_message': last_message,
            'unread_count': unread_count,
        })
    
    # Sort by last message timestamp
    conversation_data.sort(key=lambda x: x['last_message'].timestamp if x['last_message'] else timezone.now(), reverse=True)
    
    context = {
        'conversations': conversation_data,
    }
    return render(request, 'marketplace/messages/inbox.html', context)


@login_required
def conversation(request, user_id):
    """View conversation with a specific user"""
    from django.contrib.auth.models import User
    other_user = get_object_or_404(User, id=user_id)
    
    # Mark messages as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)
    
    # Get messages
    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | 
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')
    
    # Handle message sending
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = other_user
            message.save()
            messages.success(request, 'Message sent!')
            return redirect('conversation', user_id=user_id)
    else:
        form = MessageForm()
    
    context = {
        'other_user': other_user,
        'messages_list': messages_list,
        'form': form,
    }
    return render(request, 'marketplace/messages/conversation.html', context)


@login_required
def send_message(request, user_id):
    """Send a message to a user"""
    from django.contrib.auth.models import User
    receiver = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, 'Message sent!')
            return redirect('conversation', user_id=user_id)
    
    return redirect('conversation', user_id=user_id)
