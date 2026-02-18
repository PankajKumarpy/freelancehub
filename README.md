# Freelance Marketplace

A complete freelance marketplace web application built with Django, similar to Fiverr/Upwork. This platform allows freelancers to offer services (gigs) and clients to post jobs with a bidding system.

## Features

### User System
- **Dual Role Registration**: Users can register as Freelancers or Clients
- **Profile Management**: Separate profiles for freelancers and clients
- **Authentication**: Built-in Django authentication with login/logout

### For Freelancers
- Create and manage gigs (services)
- Browse and bid on jobs
- Track earnings and ratings
- Manage orders and deliveries
- Real-time messaging with clients

### For Clients
- Browse and purchase gigs
- Post jobs and receive bids
- Accept bids and create orders
- Leave reviews and ratings
- Real-time messaging with freelancers

### Core Features
- **Gig Marketplace**: Browse, search, and filter services
- **Job Posting System**: Post jobs and receive proposals
- **Bidding System**: Freelancers can bid on jobs
- **Order Management**: Track order status from creation to completion
- **Messaging System**: Direct communication between users
- **Review & Rating System**: Rate completed orders
- **Category System**: Organize gigs and jobs by categories
- **Search & Filters**: Find gigs by keywords, category, and price
- **Responsive Design**: Modern Bootstrap 5 UI

## Tech Stack

- **Backend**: Python 3.x, Django 6.0
- **Database**: SQLite (default, PostgreSQL-ready)
- **Frontend**: HTML, CSS, Bootstrap 5
- **Template Engine**: Django Template Language (DTL)
- **Image Processing**: Pillow

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Navigate to Project
```bash
cd c:\Users\pksut\vscodepy\Coding\coding
```

### Step 2: Install Dependencies
```bash
pip install django pillow
```

### Step 3: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 5: Create Sample Categories (Optional)
Access the admin panel at `http://127.0.0.1:8000/admin/` and add categories like:
- Web Development
- Graphic Design
- Content Writing
- Digital Marketing
- Video Editing
- Mobile Development

### Step 6: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

```
freelance_marketplace/
├── freelance_marketplace/          # Project configuration
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Main URL configuration
│   └── wsgi.py                     # WSGI configuration
├── marketplace/                    # Main application
│   ├── models.py                   # Database models
│   ├── views.py                    # View logic
│   ├── urls.py                     # App URL patterns
│   ├── forms.py                    # Form definitions
│   ├── admin.py                    # Admin configuration
│   ├── signals.py                  # Signal handlers
│   └── templates/                  # HTML templates
│       └── marketplace/
│           ├── base.html           # Base template
│           ├── navbar.html         # Navigation bar
│           ├── home.html           # Home page
│           ├── auth/               # Authentication templates
│           ├── gigs/               # Gig templates
│           ├── jobs/               # Job templates
│           ├── dashboard/          # Dashboard templates
│           ├── profile/            # Profile templates
│           ├── messages/           # Messaging templates
│           └── orders/             # Order templates
├── static/                         # Static files (CSS, JS)
├── media/                          # User uploads
│   ├── profiles/                   # Profile pictures
│   └── gigs/                       # Gig images
└── manage.py                       # Django management script
```

## Database Models

### User Profiles
- **FreelancerProfile**: Skills, bio, hourly rate, rating, earnings
- **ClientProfile**: Company name, contact info

### Core Models
- **Category**: Service/job categories
- **Gig**: Services offered by freelancers
- **Job**: Jobs posted by clients
- **Bid**: Freelancer proposals on jobs
- **Order**: Created when gig purchased or bid accepted
- **Message**: User-to-user messaging
- **Review**: Ratings and reviews for completed orders

## Usage Guide

### As a Freelancer
1. Register and select "Freelancer" role
2. Complete your profile with skills and bio
3. Create gigs to offer your services
4. Browse jobs and submit bids
5. Manage orders and deliver work
6. Build your rating through quality work

### As a Client
1. Register and select "Client" role
2. Complete your profile
3. Browse gigs and purchase services
4. Post jobs and review bids
5. Accept bids to create orders
6. Leave reviews after completion

## Key URLs

- `/` - Home page
- `/register/` - User registration
- `/login/` - User login
- `/gigs/` - Browse gigs
- `/gigs/create/` - Create new gig (freelancers only)
- `/jobs/` - Browse jobs
- `/jobs/create/` - Post new job (clients only)
- `/dashboard/` - User dashboard
- `/orders/` - Order management
- `/messages/` - Messaging inbox
- `/profile/` - View profile
- `/admin/` - Admin panel

## Business Logic

### Bidding System
- Freelancers can submit one bid per job
- Only one bid can be accepted per job
- Accepting a bid creates an order and updates job status
- Other bids are automatically rejected

### Order Flow
1. **Creation**: Order created when gig purchased or bid accepted
2. **In Progress**: Work is being done
3. **Completion**: Client marks order as complete
4. **Review**: Client can leave a review

### Rating System
- Reviews are 1-5 stars
- Freelancer rating auto-updates based on reviews
- Only clients can leave reviews
- Reviews only allowed after order completion

### Permissions
- Only freelancers can create gigs and bid on jobs
- Only clients can purchase gigs and post jobs
- Only order participants can view order details
- Only job owners can accept bids

## Admin Panel

Access at `/admin/` with superuser credentials.

Features:
- Manage all users, profiles, gigs, jobs, orders
- View and moderate content
- Search and filter capabilities
- Bulk actions

## Customization

### Adding Categories
1. Access admin panel
2. Go to Categories
3. Add new categories with name and description

### Changing Colors
Edit the CSS variables in `marketplace/templates/marketplace/base.html`:
```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #ec4899;
    /* ... */
}
```

### Database Migration to PostgreSQL
Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` for production
- Use environment variables for sensitive data
- Enable HTTPS in production

## Troubleshooting

### Pillow Installation Error
```bash
pip install Pillow
```

### Migration Issues
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

## Future Enhancements

- Payment integration (Stripe, PayPal)
- Email notifications
- Advanced search with Elasticsearch
- Real-time chat with WebSockets
- File upload for deliverables
- Dispute resolution system
- Freelancer verification badges
- Portfolio showcase

## License

This project is open-source and available for educational purposes.

## Support

For issues or questions, please create an issue in the project repository.

---

**Built with ❤️ using Django**
