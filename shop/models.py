from symtable import Class
from unicodedata import category

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {str(self.email)} {self.is_admin}"


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return f"{self.title} {self.image}"

class Brand(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='brands/')
    description = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.title} {self.image} {self.description}"

class Product(models.Model):
    title = models.CharField(max_length=100)
    image1 = models.ImageField(upload_to='products/', null=True, blank=True)
    image2 = models.ImageField(upload_to='products/', null=True, blank=True)
    image3 = models.ImageField(upload_to='products/', null=True, blank=True)
    image4 = models.ImageField(upload_to='products/', null=True, blank=True)
    image5 = models.ImageField(upload_to='products/', null=True, blank=True)
    characteristics = models.TextField(max_length=1500)
    description = models.TextField(max_length=1500, default="Нет описания")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.title} {self.description} {self.category} {self.count} {self.price} {self.image} {self.brand}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    review = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} {self.user} {self.rating} {self.review} {self.created_at}"
