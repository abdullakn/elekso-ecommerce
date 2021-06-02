from products.models import NormalCoupen, Product_Table
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .utils import generate_ref_code



# Create your models here.

class UserData(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number=PhoneNumberField()


class UserAddress(models.Model):
    user=models.ForeignKey(UserData,on_delete=models.CASCADE)  
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address_line1=models.CharField(max_length=50)
    address_line2=models.CharField(max_length=50,blank=True)
    
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)  


    def __str__(self):
        return self.first_name

class UserPropic(models.Model):
    user=models.OneToOneField(UserData,on_delete=models.CASCADE) 
    pro_pic=models.ImageField(upload_to='pro_pics', null=True, blank=True)


    def image_url(self):
        try:
            url=self.pro_pic.url
        except:
            url='/images/avatar.jpg'
        return url    


class ReviewRating(models.Model):
    product=models.ForeignKey(Product_Table,on_delete=models.CASCADE)
    user=models.ForeignKey(UserData,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.CharField(max_length=500,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=100,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.subject



class Referal(models.Model):
    user=models.OneToOneField(UserData,on_delete=models.CASCADE)
    code=models.CharField(max_length=12,blank=True)
    recommended_by=models.ForeignKey(UserData,on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    updated=models.DateTimeField(auto_now_add=True) 
    created=models.DateTimeField(auto_now_add=True,blank=True,null=True) 

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_recommended_profiles(self):
        qs=Referal.objects.all()
        # my_recs=[p for p in qs if p.recommended_by == self.user]
        my_recs=[]
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)

    def save(self,*args,**kwargs):
        if self.code=="":
            code=generate_ref_code()
            self.code=code

        super().save(*args,**kwargs)   


class ReferalCoupen(models.Model):
     user=models.ForeignKey(UserData,on_delete=models.CASCADE) 
     coupen_code=models.CharField(max_length=12,blank=True)
     discount=models.IntegerField(default=20)   


     def __str__(self):
         return self.coupen_code    



class UsedOffer(models.Model):
    user=models.ForeignKey(UserData,on_delete=models.CASCADE)
    coupen=models.ForeignKey(NormalCoupen,on_delete=models.CASCADE)         







