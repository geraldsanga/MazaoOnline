from django.contrib import admin
from .models import (Category, Product, OrderProduct, 
    BillingAddress, Payment, Contact, Order, ProductReview
    )
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(BillingAddress)
admin.site.register(Payment)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(ProductReview)
