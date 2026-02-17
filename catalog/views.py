from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def category_list(request):
    """Список корневых категорий."""
    categories = Category.objects.filter(is_active=True, parent__isnull=True)
    return render(request, 'catalog/category_list.html', {'categories': categories})


def category_detail(request, slug):
    """Товары в конкретной категории."""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)
    return render(
        request,
        'catalog/category_detail.html',
        {'category': category, 'products': products},
    )


def product_detail(request, slug):
    """Детальная страница товара."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_search(request):
    """Поиск по товарам."""
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(
        request,
        'catalog/search_results.html',
        {'products': products, 'query': query},
    )
