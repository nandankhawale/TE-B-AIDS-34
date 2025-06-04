from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .utils import TestServerClient, NumberStorage
import time

@api_view(['GET'])
def calculate_average(request, number_id):
   
    start_time = time.time()
    
 
    valid_categories = ['p', 'f', 'e', 'r']
    if number_id not in valid_categories:
        return Response(
            {'error': 'Invalid number ID. Use p, f, e, or r'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
   
    prev_numbers = NumberStorage.get_window_numbers(number_id, settings.WINDOW_SIZE)
    
    
    client = TestServerClient()
    new_numbers = client.fetch_numbers(number_id)
    
  
    if new_numbers:
        NumberStorage.store_numbers(number_id, new_numbers)
        NumberStorage.cleanup_old_numbers(number_id, settings.WINDOW_SIZE)
    
   
    current_numbers = NumberStorage.get_window_numbers(number_id, settings.WINDOW_SIZE)
    
  
    if current_numbers:
        avg = sum(current_numbers) / len(current_numbers)
        avg = round(avg, 2)
    else:
        avg = 0
   
    response_data = {
        "windowPrevState": list(reversed(prev_numbers)),  
        "windowCurrState": list(reversed(current_numbers)),
        "numbers": new_numbers,
        "avg": avg
    }
    
 
    elapsed_time = time.time() - start_time
    if elapsed_time > 0.5:
        print(f"Warning: Response time exceeded 500ms: {elapsed_time:.3f}s")
    
    return Response(response_data)

@api_view(['GET'])
def health_check(request):
    
    return Response({
        'status': 'healthy',
        'timestamp': time.time(),
        'window_size': settings.WINDOW_SIZE
    })

