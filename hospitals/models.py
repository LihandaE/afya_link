from django.db import models

# Create your models here.

class Hospital(models.Model):
    name= models.CharField(max_length=260)
    location =models.CharField(max_length=260)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
