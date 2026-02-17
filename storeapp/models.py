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
class orders(models.Model):
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    user = models.ForeignKey(users,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,default='pending')
    def __str__(self):
        return f"Order {self.id} by {self.user.name}" 