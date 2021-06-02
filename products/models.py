# from accounts.models import UserData
from django.db.models.aggregates import Avg
# from accounts.models import ReviewRating
from django.db import models
from django.urls import reverse
from django.db.models import Avg

from datetime import date
# from accounts.models import *



# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug=models.SlugField(unique=True)


    def __str__(self):
        return self.name

class Brand(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='related_category')
    brand=models.CharField(max_length=50)

    def __str__(self):
        return self.brand

class Product_Table(models.Model):


    RAM=(

        ('4','4'),
        ('8','8'),
        ('12','12'),
        ('16','16')
    )


    STORAGE=(

        ('32 GB','32 GB'),
        ('64 GB','64 GB'),
        ('128 GB','128 GB'),
        ('256 GB','256 GB'),
        ('512 GB','512 GB'),
        

    )






    product_name = models.CharField(max_length=50,default="")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)  
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    
    price=models.IntegerField()
    offer_price=models.FloatField(null=True)
    offer_percentage=models.FloatField(null=True)
    stock=models.IntegerField()
    description=models.CharField(max_length=500,default="")
    processor=models.CharField(max_length=30,default="") 
    ram=models.CharField(max_length=20,choices=RAM)
    storage=models.CharField(max_length=20,choices=STORAGE)
    screen_size=models.IntegerField(default='') 
    color=models.CharField(max_length=30,default='')
    slug=models.SlugField(unique=True)
    image1 = models.ImageField(upload_to='prd_img', null=True, blank=True)
    image2 = models.ImageField(upload_to='prd_img', null=True, blank=True)
    image3 = models.ImageField(upload_to='prd_img', null=True, blank=True)
    image4 = models.ImageField(upload_to='prd_img', null=True, blank=True)

    def __str__(self):
        return self.product_name

    def product_offer(self):
        today = date.today()
        today1 = today.strftime("%Y-%m-%d")
        print("product offer function")
        print(today1)
    
        offer=ProductOffer.objects.get(product=self.id) 
        print("befeore offer obj")
        print(offer.offer)
        print("after offer obj")
        print(offer.offer_end)
        if str(offer.offer_end) >= today1:
            print("in if")
            return offer.offer
        else:
            print("false")
            return "False"    
        
          

    # def averageReview(self):
    #     reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))  
    #     avg=0
    #     if reviews['average'] is not None:
    #         avg=float(reviews['average'])
    #     return avg    

    # def get_url(self):
    #     return reverse('product_details',args=[self.slug])


class CategoryOffer(models.Model):
    category=models.OneToOneField(Category,on_delete=models.CASCADE)
    offer=models.IntegerField()
    offer_start=models.DateField()
    offer_end=models.DateField()


    def check_expired(self):
        today = date.today()
        today1 = today.strftime("%Y-%m-%d")
        if str(self.offer_end)<= today1:
            return False
        else:
            return True   

class ProductOffer(models.Model):
    product=models.OneToOneField(Product_Table,on_delete=models.CASCADE)
    offer=models.IntegerField()
    offer_start=models.DateField()
    offer_end=models.DateField()



    def check_expired(self):
        today = date.today()
        today1 = today.strftime("%Y-%m-%d")
        if str(self.offer_end)<= today1:
            return False
        else:
            return True   

#not used check_expired



class NormalCoupen(models.Model):
    coupen_title=models.CharField(max_length=30)  
    coupen_code=models.CharField(max_length=30)
    coupen_offer=models.FloatField()
    validity=models.BooleanField(default=True)






    

    





