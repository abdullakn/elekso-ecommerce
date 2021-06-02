from django.contrib import admin

from products.models import *

# Register your models here.


admin.site.register(Product_Table)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(NormalCoupen)

