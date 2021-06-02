from django.db.models import fields
from accounts import models
from django import forms

from products.models import Brand,Category,Product_Table,CategoryOffer
from order.models import OrderProduct



class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product_Table
        exclude=('offer_price','offer_percentage',)
        widgets = {
            'price': forms.TextInput(attrs={'type': 'number','class':'price'}),
        }
        # fields = '__all__'
        # fields=['product_name','category','brand','price','stock','description','processor','ram','storage','screen_size','color','slug','image1','image2','image3','image4']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['brand'].queryset = Brand.objects.filter(category_id=category_id).order_by('brand')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            
            
            
            # self.fields['brand'].queryset = self.instance.category.brand_set.order_by('brand')
            self.fields['brand'].queryset = Brand.objects.filter(category_id=self.instance.category.id).order_by('brand')


class OfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields = '__all__'
        labels = {
        "offer": "Offer in Percentage"
    }