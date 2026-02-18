"""
Script to create comprehensive test data for the Freelance Marketplace
"""
import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelance_marketplace.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from marketplace.models import (
    FreelancerProfile, ClientProfile, Category, Gig, Job, 
    Bid, Order, Message, Review
)

print("Creating test data for Freelance Marketplace...\n")

# Create test users
print("1. Creating test users...")

# Freelancers
freelancer1, created = User.objects.get_or_create(
    username='john_dev',
    defaults={
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Developer'
    }
)
if created:
    freelancer1.set_password('password123')
    freelancer1.save()
    FreelancerProfile.objects.create(
        user=freelancer1,
        skills='Python, Django, JavaScript, React',
        bio='Full-stack developer with 5 years of experience',
        experience=5,
        hourly_rate=50.00
    )
    print(f"   ✓ Created freelancer: {freelancer1.username}")

freelancer2, created = User.objects.get_or_create(
    username='sarah_design',
    defaults={
        'email': 'sarah@example.com',
        'first_name': 'Sarah',
        'last_name': 'Designer'
    }
)
if created:
    freelancer2.set_password('password123')
    freelancer2.save()
    FreelancerProfile.objects.create(
        user=freelancer2,
        skills='UI/UX Design, Figma, Adobe XD, Photoshop',
        bio='Creative designer specializing in modern UI/UX',
        experience=3,
        hourly_rate=40.00
    )
    print(f"   ✓ Created freelancer: {freelancer2.username}")

# Clients
client1, created = User.objects.get_or_create(
    username='tech_startup',
    defaults={
        'email': 'contact@techstartup.com',
        'first_name': 'Tech',
        'last_name': 'Startup'
    }
)
if created:
    client1.set_password('password123')
    client1.save()
    ClientProfile.objects.create(
        user=client1,
        company_name='Tech Startup Inc.',
        contact_info='contact@techstartup.com'
    )
    print(f"   ✓ Created client: {client1.username}")

client2, created = User.objects.get_or_create(
    username='ecommerce_co',
    defaults={
        'email': 'info@ecommerce.com',
        'first_name': 'Ecommerce',
        'last_name': 'Company'
    }
)
if created:
    client2.set_password('password123')
    client2.save()
    ClientProfile.objects.create(
        user=client2,
        company_name='Ecommerce Solutions Ltd.',
        contact_info='info@ecommerce.com'
    )
    print(f"   ✓ Created client: {client2.username}")

print(f"\n2. Creating sample gigs...")

# Get categories
web_dev = Category.objects.get(name='Web Development')
ui_ux = Category.objects.get(name='UI/UX Design')
mobile = Category.objects.get(name='Mobile Development')

# Create gigs
gig1, created = Gig.objects.get_or_create(
    freelancer=freelancer1,
    title='Full-Stack Web Application Development',
    defaults={
        'description': 'I will develop a complete web application using Django and React. Includes backend API, database design, and responsive frontend.',
        'category': web_dev,
        'price': 500.00,
        'delivery_time': 14,
        'is_active': True
    }
)
if created:
    print(f"   ✓ Created gig: {gig1.title}")

gig2, created = Gig.objects.get_or_create(
    freelancer=freelancer1,
    title='Django REST API Development',
    defaults={
        'description': 'Professional REST API development with Django REST Framework. Includes authentication, documentation, and testing.',
        'category': web_dev,
        'price': 300.00,
        'delivery_time': 7,
        'is_active': True
    }
)
if created:
    print(f"   ✓ Created gig: {gig2.title}")

gig3, created = Gig.objects.get_or_create(
    freelancer=freelancer2,
    title='Modern UI/UX Design for Web Apps',
    defaults={
        'description': 'Complete UI/UX design including wireframes, mockups, and interactive prototypes using Figma.',
        'category': ui_ux,
        'price': 400.00,
        'delivery_time': 10,
        'is_active': True
    }
)
if created:
    print(f"   ✓ Created gig: {gig3.title}")

gig4, created = Gig.objects.get_or_create(
    freelancer=freelancer2,
    title='Logo and Brand Identity Design',
    defaults={
        'description': 'Professional logo design with complete brand identity package including color palette and typography.',
        'category': ui_ux,
        'price': 250.00,
        'delivery_time': 5,
        'is_active': True
    }
)
if created:
    print(f"   ✓ Created gig: {gig4.title}")

print(f"\n3. Creating sample jobs...")

# Create jobs
job1, created = Job.objects.get_or_create(
    client=client1,
    title='E-commerce Website Development',
    defaults={
        'description': 'Need a full-featured e-commerce website with payment integration, product management, and user authentication.',
        'category': web_dev,
        'budget': 2000.00,
        'deadline': timezone.now().date() + timedelta(days=30),
        'status': 'Open'
    }
)
if created:
    print(f"   ✓ Created job: {job1.title}")

job2, created = Job.objects.get_or_create(
    client=client2,
    title='Mobile App UI/UX Redesign',
    defaults={
        'description': 'Looking for a designer to redesign our mobile app interface with modern, user-friendly design.',
        'category': ui_ux,
        'budget': 800.00,
        'deadline': timezone.now().date() + timedelta(days=20),
        'status': 'Open'
    }
)
if created:
    print(f"   ✓ Created job: {job2.title}")

job3, created = Job.objects.get_or_create(
    client=client1,
    title='API Integration for Mobile App',
    defaults={
        'description': 'Need to integrate third-party APIs into our existing mobile application.',
        'category': mobile,
        'budget': 600.00,
        'deadline': timezone.now().date() + timedelta(days=15),
        'status': 'Open'
    }
)
if created:
    print(f"   ✓ Created job: {job3.title}")

print(f"\n4. Creating sample bids...")

# Create bids
bid1, created = Bid.objects.get_or_create(
    job=job1,
    freelancer=freelancer1,
    defaults={
        'proposal_text': 'I have 5 years of experience building e-commerce websites. I can deliver a high-quality solution with all requested features.',
        'bid_amount': 1800.00,
        'delivery_days': 25,
        'status': 'Pending'
    }
)
if created:
    print(f"   ✓ Created bid from {freelancer1.username} on {job1.title}")

bid2, created = Bid.objects.get_or_create(
    job=job2,
    freelancer=freelancer2,
    defaults={
        'proposal_text': 'I specialize in mobile UI/UX design. I will create a modern, intuitive design that your users will love.',
        'bid_amount': 750.00,
        'delivery_days': 18,
        'status': 'Pending'
    }
)
if created:
    print(f"   ✓ Created bid from {freelancer2.username} on {job2.title}")

print(f"\n5. Creating sample order (completed)...")

# Create a completed order with review
order1, created = Order.objects.get_or_create(
    client=client1,
    freelancer=freelancer2,
    gig=gig4,
    defaults={
        'price': 250.00,
        'status': 'Completed',
        'completed_at': timezone.now()
    }
)
if created:
    print(f"   ✓ Created completed order for {gig4.title}")
    
    # Create review
    review1, created_review = Review.objects.get_or_create(
        order=order1,
        defaults={
            'rating': 5,
            'review_text': 'Excellent work! The logo design exceeded my expectations. Very professional and creative.'
        }
    )
    if created_review:
        print(f"   ✓ Created 5-star review for the order")

print(f"\n6. Creating sample messages...")

# Create messages
msg1, created = Message.objects.get_or_create(
    sender=client1,
    receiver=freelancer1,
    content='Hi John, I saw your web development gig. Can you handle a large e-commerce project?',
    defaults={'is_read': True}
)
if created:
    print(f"   ✓ Created message from {client1.username} to {freelancer1.username}")

msg2, created = Message.objects.get_or_create(
    sender=freelancer1,
    receiver=client1,
    content='Hello! Yes, I have extensive experience with e-commerce projects. I would be happy to discuss your requirements.',
    defaults={'is_read': True}
)
if created:
    print(f"   ✓ Created reply from {freelancer1.username} to {client1.username}")

msg3, created = Message.objects.get_or_create(
    sender=client1,
    receiver=freelancer2,
    content='Thank you for the amazing logo design! I love it!',
    defaults={'is_read': False}
)
if created:
    print(f"   ✓ Created message from {client1.username} to {freelancer2.username}")

print("\n" + "="*60)
print("✅ Test data created successfully!")
print("="*60)

print("\n📊 Summary:")
print(f"   • Users: {User.objects.count()} total")
print(f"   • Freelancers: {FreelancerProfile.objects.count()}")
print(f"   • Clients: {ClientProfile.objects.count()}")
print(f"   • Categories: {Category.objects.count()}")
print(f"   • Gigs: {Gig.objects.count()}")
print(f"   • Jobs: {Job.objects.count()}")
print(f"   • Bids: {Bid.objects.count()}")
print(f"   • Orders: {Order.objects.count()}")
print(f"   • Reviews: {Review.objects.count()}")
print(f"   • Messages: {Message.objects.count()}")

print("\n🔑 Test Login Credentials:")
print("\n   Admin:")
print("   • Username: admin")
print("   • Password: admin123")
print("\n   Freelancers:")
print("   • Username: john_dev | Password: password123")
print("   • Username: sarah_design | Password: password123")
print("\n   Clients:")
print("   • Username: tech_startup | Password: password123")
print("   • Username: ecommerce_co | Password: password123")

print("\n🌐 Access the application:")
print("   • Home: http://127.0.0.1:8000/")
print("   • Admin: http://127.0.0.1:8000/admin/")
print("   • Gigs: http://127.0.0.1:8000/gigs/")
print("   • Jobs: http://127.0.0.1:8000/jobs/")
