from django.db import models
from django.contrib.auth.models import User


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
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Products'


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    country = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
