from django.db import models


class CallStatus(models.Model):
    call_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address