import os
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TrafficLog

# Create your views here.

@csrf_exempt # Bypass CSRF for API endpoint because this is a machine-to-machine communication
def ingest_log(request):
    if request.method == 'POST':
        expected_token = os.getenv('API_INGESTION_TOKEN')
        auth_header = request.headers.get('Authorization', '')
        if expected_token and auth_header != f'Bearer {expected_token}':
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        try:
            data = json.loads(request.body)
            log_entry = TrafficLog.objects.create(
                service_name=data.get('service_name', 'unknown-service'),
                method=data.get('method', 'UNKNOWN'),
                path=data.get('path', '/'),
                status_code=data.get('status_code', 200),
                remote_ip=data.get('remote_ip'),
                execution_duration=data.get('execution_duration'),
                payload=data

            )
            return JsonResponse({'status': 'success', 'log_id': str(log_entry.id)}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)