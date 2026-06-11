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
            raw_data = json.loads(request.body)

            if isinstance(raw_data,dict):
                logs_to_process = [raw_data]
            elif isinstance(raw_data,list):
                logs_to_process = raw_data
            else:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
            
            saved_ids = []
            for data in logs_to_process:
                log_entry = TrafficLog.objects.create(
                    service_name=data.get('service_name', 'UNKNOWN'),
                    method=data.get('method', 'UNKNOWN'),
                    path=data.get('path', '/'),
                    status_code=data.get('status_code', 0),
                    remote_ip=data.get('remote_ip', ''),
                    execution_duration=data.get('execution_duration', 0.0),
                    payload=data.get('payload', {})
                )
                saved_ids.append(str(log_entry.id))
            
            return JsonResponse({'status': 'success', 'count': len(saved_ids), 'ids': saved_ids}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)