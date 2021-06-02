from django.db import models
from products.models import Product_Table
from accounts.models import UserData

# Create your models here.


class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added= models.DateField(auto_now_add=True)


    def __str__(self):
        return self.cart_id



class CartItem(models.Model):
    user=models.ForeignKey(UserData,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product_Table,on_delete=models.CASCADE) 
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True) 


    def sub_total(self):
        if self.product.offer_price == None:
            return self.product.price * self.quantity
        else:
            return self.product.offer_price * self.quantity




