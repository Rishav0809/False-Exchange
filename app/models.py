from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Order(models.Model):
    security_type = models.CharField(max_length=100,default="")
    order_type= models.CharField(max_length=100,default="")
    quantity= models.IntegerField(default=0)
    price = models.FloatField(default=0)
    status = models.CharField(max_length=100,default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return self.security_type
    