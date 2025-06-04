import requests
import time
from django.conf import settings
from .models import AuthToken, NumberEntry

class TestServerClient:
    def __init__(self):
        self.base_url = settings.TEST_SERVER_BASE_URL
        self.auth_data = {
            "email": "nandankhawale555@gmail.com",
            "name": "nandan khawale",
            "rollNo": "tebai&ds-34",
            "accessCode": "KRjUUU",
            "clientID": "397efb12-24e0-4485-81f6-6dad38c6486b",
            "clientSecret": "rzddSeDRvzBtBcPy"
        }
    
    def get_valid_token(self):
        """Get a valid access token, refreshing if necessary"""
        try:
            token_obj = AuthToken.objects.latest('created_at')
            if not token_obj.is_expired:
                return token_obj.access_token
        except AuthToken.DoesNotExist:
            pass
        
        # Need to authenticate
        return self._authenticate()
    
    def _authenticate(self):
      
        try:
            response = requests.post(
                f"{self.base_url}/auth",
                json=self.auth_data,
                timeout=5
            )
            response.raise_for_status()
            
            auth_response = response.json()
            
            # Save token to database
            AuthToken.objects.create(
                access_token=auth_response['access_token'],
                token_type=auth_response['token_type'],
                expires_in=auth_response['expires_in']
            )
            
            return auth_response['access_token']
            
        except requests.RequestException as e:
            print(f"Authentication failed: {e}")
            return None
    
    def fetch_numbers(self, category):
        
        category_endpoints = {
            'p': 'primes',
            'f': 'fibo',
            'e': 'even',
            'r': 'rand'
        }
        
        if category not in category_endpoints:
            return []
        
        token = self.get_valid_token()
        if not token:
            return []
        
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            endpoint = f"{self.base_url}/{category_endpoints[category]}"
            response = requests.get(endpoint, headers=headers, timeout=0.5)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('numbers', [])
            else:
                print(f"Failed to fetch {category} numbers: {response.status_code}")
                return []
                
        except requests.Timeout:
            print(f"Timeout fetching {category} numbers")
            return []
        except requests.RequestException as e:
            print(f"Error fetching {category} numbers: {e}")
            return []

class NumberStorage:
    @staticmethod
    def store_numbers(category, numbers):
        
        stored_count = 0
        for number in numbers:
            try:
                NumberEntry.objects.get_or_create(
                    category=category,
                    number=number
                )
                stored_count += 1
            except Exception as e:
                print(f"Error storing number {number}: {e}")
        return stored_count
    
    @staticmethod
    def get_window_numbers(category, window_size):
        
        return list(
            NumberEntry.objects
            .filter(category=category)
            .order_by('-timestamp')[:window_size]
            .values_list('number', flat=True)
        )
    
    @staticmethod
    def cleanup_old_numbers(category, window_size):
        
        numbers_to_keep = (
            NumberEntry.objects
            .filter(category=category)
            .order_by('-timestamp')[:window_size]
            .values_list('id', flat=True)
        )
        
        NumberEntry.objects.filter(
            category=category
        ).exclude(id__in=numbers_to_keep).delete()