from django.db import models

# Create your models here.
class users(models.Model):
    name = models.CharField(max_length=20)
    gmail = models.CharField()
    number = models.IntegerField()
    password =models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class products(models.Model):
    product_name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='product_image')

    def __str__(self):
        return self.product_name    