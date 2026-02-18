"""
Script to fix all template syntax errors
"""

# Fix gig_list.html - category filter
gig_list_path = r'marketplace\templates\marketplace\gigs\gig_list.html'
with open(gig_list_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken template tag - category filter
content = content.replace(
    '{% if request.GET.category==category.id|stringformat:"s"\r\n                            %}selected{% endif %}',
    '{% if request.GET.category == category.id|stringformat:"s" %}selected{% endif %}'
)
content = content.replace(
    '{% if request.GET.category==category.id|stringformat:"s"\n                            %}selected{% endif %}',
    '{% if request.GET.category == category.id|stringformat:"s" %}selected{% endif %}'
)

with open(gig_list_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed gig_list.html category filter")

# Fix job_list.html - category filter
job_list_path = r'marketplace\templates\marketplace\jobs\job_list.html'
with open(job_list_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken template tag - category filter
content = content.replace(
    '{% if request.GET.category==category.id|stringformat:"s"\r\n                            %}selected{% endif %}',
    '{% if request.GET.category == category.id|stringformat:"s" %}selected{% endif %}'
)
content = content.replace(
    '{% if request.GET.category==category.id|stringformat:"s"\n                            %}selected{% endif %}',
    '{% if request.GET.category == category.id|stringformat:"s" %}selected{% endif %}'
)

# Fix status filters
content = content.replace('request.GET.status=="Open"', 'request.GET.status == "Open"')
content = content.replace('request.GET.status=="In Progress"', 'request.GET.status == "In Progress"')
content = content.replace('request.GET.status=="Completed"', 'request.GET.status == "Completed"')

with open(job_list_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Fixed job_list.html category filter and status filters")
print("\n✅ All template fixes applied successfully!")
