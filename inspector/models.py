from django.db import models

# Create your models here.
class TrafficLog(models.Model):
    
    timestamp = models.DateTimeField(auto_now_add=True)

    # Indexes
    service_name = models.CharField(max_length=100, default="unknown-service")
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    status_code = models.IntegerField(null=True, blank=True)
    remote_ip = models.GenericIPAddressField(null=True, blank=True)
    execution_duration = models.FloatField(null=True, blank=True)

    # unstructured NoSQL payload
    payload = models.JSONField(default=dict,help_text="Unstructured log data in JSON format")

    def __str__(self):
        return f"[{self.status_code}] {self.method} {self.path} - {self.remote_ip} at {self.timestamp}" 
    