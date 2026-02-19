"""
WSGI config for freelance_marketplace project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelance_marketplace.settings')



# Vercel-specific: Copy SQLite DB to /tmp if it doesn't exist
if 'VERCEL' in os.environ:
    import shutil
    from pathlib import Path
    
    # Path to where Vercel puts the source code
    # __file__ is freelance_marketplace/wsgi.py -> parent is freelance_marketplace -> parent is project root
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Source DB (committed to repo)
    db_source = BASE_DIR / 'db.sqlite3'
    # Target DB (writable /tmp)
    db_target = Path('/tmp/db.sqlite3')
    
    # Copy only if source exists and target doesn't (or always copy to reset? lets copy if missing to be safe)
    if db_source.exists() and not db_target.exists():
        try:
            shutil.copy2(db_source, db_target)
            print(f"Copied database from {db_source} to {db_target}")
        except Exception as e:
            print(f"Failed to copy database: {e}")

application = get_wsgi_application()
app = application
