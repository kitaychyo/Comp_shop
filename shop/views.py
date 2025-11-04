from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer
from django.shortcuts import render

@api_view(['GET'])
def brands_list(request):
    brands = Brand.objects.all()
    serializer = BrandSerializer(brands, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True, context={'request': request})
    return Response(serializer.data)

# @api_view(['GET'])
@api_view(['GET'])
def products_list(request):
    qs = Product.objects.all()

    # Filters
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    search = request.GET.get('q')

    if category_id:
        qs = qs.filter(category_id=category_id)
    if brand_id:
        qs = qs.filter(brand_id=brand_id)
    if price_min:
        qs = qs.filter(price__gte=price_min)
    if price_max:
        qs = qs.filter(price__lte=price_max)
    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))

    serializer = ProductSerializer(qs, many=True, context={'request': request})
    return Response(serializer.data)


def home(request):
    return render(request, 'home.html')


def products_page(request):
    return render(request, 'products.html')
