import os
from decimal import Decimal

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Document
from django.contrib.postgres.search import SearchVector
# Create the first 'Document' object with a title and content.

# Perform a full-text search for documents containing the words 'django' and 'web framework'.
results = Document.objects.filter(search_vector='3frwf')

# Print the search results.
for result in results:
    print(f"Title: {result.title}")
