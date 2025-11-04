from rest_framework import serializers
from .models import Brand, Category, Product

class BrandSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title')
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None


# class ProductSerializer(serializers.ModelSerializer):
class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    brand_name = serializers.CharField(source='brand.title', read_only=True)
    category_name = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'image', 'brand', 'brand_name', 'category', 'category_name']

    def get_image(self, obj):
        request = self.context.get('request')
        # Pick first available image among image1..image5
        for field in ('image1', 'image2', 'image3', 'image4', 'image5'):
            img = getattr(obj, field, None)
            if img:
                url = img.url
                return request.build_absolute_uri(url) if request else url
        return None
