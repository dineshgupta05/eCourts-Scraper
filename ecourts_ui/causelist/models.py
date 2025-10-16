from django.db import models

class DownloadLog(models.Model):
    state = models.CharField(max_length=200, blank=True)
    district = models.CharField(max_length=200, blank=True)
    complex_name = models.CharField(max_length=200, blank=True)
    court_name = models.CharField(max_length=400, blank=True)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.state} | {self.district} | {self.complex_name} | {self.court_name} | {self.date}"
