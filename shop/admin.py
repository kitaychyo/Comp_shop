from django.contrib import admin
from .models import User, Category, Product, Review, Brand

# Регистрируем модели, чтобы они отображались в админке
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Brand)
# Register your models here.
