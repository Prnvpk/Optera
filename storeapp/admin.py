from django.contrib import admin
from .models import users,products,orders

# Register your models here.
admin.site.register(users)
admin.site.register(products)
admin.site.register(orders)
