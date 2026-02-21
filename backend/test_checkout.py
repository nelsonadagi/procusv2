import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()
buyer = User.objects.get(email='buyer@gov.ke') # assumed email
client = Client()
client.force_login(buyer)
resp = client.post('/api/orders/quote-requests/3/checkout/', {'response_id': 1}, content_type='application/json')
print(resp.status_code)
print(resp.content)
