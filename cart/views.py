from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Product


def _get_cart(session):
    """
    Возвращает корзину из сессии в виде dict:
    {product_id: {'quantity': int}}
    """
    return session.setdefault('cart', {})


def cart_detail(request):
    cart = _get_cart(request.session)
    items = []
    total = 0

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    products_map = {p.id: p for p in products}

    for product_id, data in cart.items():
        product = products_map.get(int(product_id))
        if not product:
            continue
        quantity = data.get('quantity', 1)
        price = product.get_price()
        line_total = price * quantity
        total += line_total
        items.append(
            {
                'product': product,
                'quantity': quantity,
                'price': price,
                'line_total': line_total,
            }
        )

    return render(
        request,
        'cart/detail.html',
        {
            'cart_items': items,
            'cart_total': total,
        },
    )


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request.session)
    item = cart.get(str(product.id), {'quantity': 0})
    item['quantity'] = item.get('quantity', 0) + 1
    cart[str(product.id)] = item
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'cart:detail'))


def cart_remove(request, product_id):
    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect('cart:detail')

