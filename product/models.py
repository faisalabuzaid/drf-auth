from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

class Product(models.Model):
    purchaser = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        reverse('product_detail', args=[str(self.id)])