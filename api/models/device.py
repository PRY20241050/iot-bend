from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100, blank=True)
    description = models.TextField(max_length=500, blank=True)
    status = models.BooleanField(default=False)
    battery_level = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    last_update = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # @property
    # def status_text(self):
    #     return 'On' if self.status else 'Off'
    
    # def get_number(self):
    #     return 100

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'device'
