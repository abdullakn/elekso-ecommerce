from django import forms

from products.models import Brand,Category,Product_Table


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product_Table
        fields = '__all__'

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
            self.fields['brand'].queryset = self.instance.category.brand_set.order_by('brand')