from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug=models.SlugField(unique=True)


    def __str__(self):
        return self.name

class Brand(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    brand=models.CharField(max_length=50)

    def __str__(self):
        return self.brand

class Product_Table(models.Model):
    product_name = models.CharField(max_length=50,default="")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)  
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    
    price=models.IntegerField()
    stock=models.IntegerField()
    description=models.CharField(max_length=500,default="")
    processor=models.CharField(max_length=30,default="") 
    ram=models.IntegerField()
    storage=models.IntegerField(default='')
    screen_size=models.IntegerField(default='') 
    color=models.CharField(max_length=30,default='')
    slug=models.SlugField(unique=True)
    image1 = models.ImageField(upload_to='prd_img', null=True, blank=True)
    image2 = models.ImageField(upload_to='prd_img', null=True, blank=True)
    image3 = models.ImageField(upload_to='prd_img', null=True, blank=True)
    image4 = models.ImageField(upload_to='prd_img', null=True, blank=True)



    def get_url(self):
        return reverse('product_details',args=[self.slug])




    

    





