import os
import json
import random
import time
import requests

API_URL = os.getenv("INGESTION_API_URL", "http://localhost:8000/api/v1/mock-log/")
API_TOKEN = os.getenv("API_INGESTION_TOKEN", "super-secure-homelab-token-123")

SERVICES = ["auth-service", "payment-gateway", "frontend-router", "user-profile-api", "inventory-v2"]
METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
PATHS = [
    "/api/v1/login", "/api/v1/checkout", "/users/profile/edit", 
    "/products/items", "/static/assets/logo.png", "/api/v1/signup",
    "/billing/invoice/download", "/metrics", "/healthz"
]
STATUS_CODES = [200, 201, 204, 400, 401, 403, 404, 500, 502]
IPS = ["192.168.1.25", "10.0.0.15", "172.16.4.2", "8.8.8.8", "109.224.11.83"]

def generate_mock_log():
    method = random.choice(METHODS)
    path = random.choice(PATHS)
    status = random.choice(STATUS_CODES)
    if "login" in path and status == 201:
        status = 200
    if "checkout" in path and method == "GET":
        method = "POST"
    
    payload = {
        "service_name": random.choice(SERVICES),
        "method": method,
        "path": path,
        "status_code": status,
        "remote_ip": random.choice(IPS),
        "execution_duration": round(random.uniform(5.2, 480.8), 2),
        # Nested Unstructured Data
        "traefik_internal": {
            "router_rule": f"PathPrefix(`{path.split('/')[1] if len(path.split('/')) > 1 else ''}`)",
            "overhead_ms": round(random.uniform(0.1, 2.5), 4),
            "tls_enabled": random.choice([True, False])
        },
        "user_agent_raw": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    return payload

def fire_traffic(count=50):
    "Send a burst of mock traffic logs to the API endpoint"
    print(f"Firing {count} mock log entries to {API_URL}")
    success_count = 0
    for i in range(1,count+1):
        log_data = generate_mock_log()
        headers = {"Authorization": f"Bearer {API_TOKEN}"} if API_TOKEN else {}
        try:
            response = requests.post(API_URL, json=log_data, headers=headers, timeout=5)
            if response.status_code == 201:
                success_count += 1
                print(f"[{i}/{count}] Status {log_data['status_code']} -> Sent successfully to Mongo.")
            else:
                print(f"❌ [{i}/{count}] Failed with server status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ [{i}/{count}] Connection error. Is the server running?")
            break
        time.sleep(random.uniform(0.05, 0.2))
    print(f"Finished firing traffic. Successfully sent {success_count}/{count} logs.")

if __name__ == "__main__":
    fire_traffic(100)
