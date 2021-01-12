from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    price = models.IntegerField(verbose_name="Price(Tshs)")
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "slug": self.slug
            }
        )
    
    def remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "slug": self.slug
            }
        )

    class Meta:
        verbose_name_plural = 'Products'


class OrderProduct(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return f"{self.quantity} {self.product.name}"
    
    def get_total_product_price(self)->int:
        return self.quantity * self.product.price
    
    def total_item_price(self)->int:
        return self.quantity*self.product.price
    
    def get_final_price(self):
        return self.total_item_price()
    


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(OrderProduct)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField()


    def __str__(self):
        return f"#{self.id}-Order by {self.customer} - {self.ordered_date.date()}"
    
    def get_total(self)->int:
        total = int()
        for product_order in self.product.all():
            total += product_order.get_total_product_price()
        return total
    
   
class BillingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    country = CountryField(multiple=False)
    city = models.CharField(max_length=50)
    street_address = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.customer.username
    
    class Meta:
        ordering = [
            "-id"
        ]
    

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    customer = models.ForeignKey(User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.customer.username
    
    class Meta:
        ordering = [
            "-id"
        ]

class Contact(models.Model):
    phone = models.CharField(max_length=13, null=True, blank=True)
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.phone


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField(max_length=255, null=True)
    rating = models.IntegerField(default=1)
    date_reviewed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"review for {self.product} by {self.user}"


class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return f"{self.name}-{self.location}"


class CurrentOrderStore(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    ordered_product = models.ManyToManyField(Order)
    date_received = models.DateTimeField()

    def __str__(self):
        return f"{self.ordered_product} currently in {self.store}"
    
    class Meta:
        ordering = (
            "-id",
        )
    