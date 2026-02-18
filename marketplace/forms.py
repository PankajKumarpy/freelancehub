from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FreelancerProfile, ClientProfile, Gig, Job, Bid, Message, Review


class UserRegistrationForm(UserCreationForm):
    """User registration form with role selection"""
    ROLE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    ]
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, widget=forms.RadioSelect)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': ''})


class FreelancerProfileForm(forms.ModelForm):
    """Form for freelancer profile"""
    class Meta:
        model = FreelancerProfile
        fields = ['profile_picture', 'skills', 'bio', 'experience', 'hourly_rate']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Python, Django, JavaScript'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'profile_picture':
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class ClientProfileForm(forms.ModelForm):
    """Form for client profile"""
    class Meta:
        model = ClientProfile
        fields = ['profile_picture', 'company_name', 'contact_info']
        widgets = {
            'contact_info': forms.TextInput(attrs={'placeholder': 'Email or phone number'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'profile_picture':
                self.fields[field].widget.attrs.update({'class': 'form-control'})


class GigForm(forms.ModelForm):
    """Form for creating/editing gigs"""
    class Meta:
        model = Gig
        fields = ['title', 'description', 'category', 'price', 'delivery_time', 'image', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your service in detail...'}),
            'delivery_time': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Days'}),
            'price': forms.NumberInput(attrs={'min': 1, 'placeholder': 'e.g. 999'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ['image', 'is_active']:
                continue
            elif hasattr(field.widget, 'choices'):
                # Select/dropdown widgets
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price


class JobForm(forms.ModelForm):
    """Form for posting jobs"""
    class Meta:
        model = Job
        fields = ['title', 'description', 'budget', 'deadline', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe the job requirements...'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'budget': forms.NumberInput(attrs={'min': 1, 'placeholder': 'e.g. 5000'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'choices'):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget and budget <= 0:
            raise forms.ValidationError("Budget must be greater than 0")
        return budget


class BidForm(forms.ModelForm):
    """Form for submitting bids"""
    class Meta:
        model = Bid
        fields = ['proposal_text', 'bid_amount', 'delivery_days']
        widgets = {
            'proposal_text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Explain why you are the best fit for this job...'}),
            'delivery_days': forms.NumberInput(attrs={'min': 1, 'placeholder': 'Days'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_bid_amount(self):
        bid_amount = self.cleaned_data.get('bid_amount')
        if bid_amount and bid_amount <= 0:
            raise forms.ValidationError("Bid amount must be greater than 0")
        return bid_amount


class MessageForm(forms.ModelForm):
    """Form for sending messages"""
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control'})


class ReviewForm(forms.ModelForm):
    """Form for submitting reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'review_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review_text'].widget.attrs.update({'class': 'form-control'})
