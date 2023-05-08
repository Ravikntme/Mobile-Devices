from django.db import models

# Create your models here.

class Mobile(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.brand