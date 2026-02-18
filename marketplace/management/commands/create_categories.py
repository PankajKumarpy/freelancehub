"""
Management command to create sample categories
"""
from django.core.management.base import BaseCommand
from marketplace.models import Category


class Command(BaseCommand):
    help = 'Creates sample categories for the marketplace'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Web Development',
                'description': 'Website development, web applications, and web design services'
            },
            {
                'name': 'Mobile Development',
                'description': 'iOS, Android, and cross-platform mobile app development'
            },
            {
                'name': 'Graphic Design',
                'description': 'Logo design, branding, illustrations, and visual design'
            },
            {
                'name': 'Content Writing',
                'description': 'Blog posts, articles, copywriting, and content creation'
            },
            {
                'name': 'Digital Marketing',
                'description': 'SEO, social media marketing, email marketing, and advertising'
            },
            {
                'name': 'Video Editing',
                'description': 'Video production, editing, animation, and post-production'
            },
            {
                'name': 'Data Science',
                'description': 'Data analysis, machine learning, AI, and statistical modeling'
            },
            {
                'name': 'UI/UX Design',
                'description': 'User interface design, user experience, and product design'
            },
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('\nSuccessfully created sample categories!')
        )
