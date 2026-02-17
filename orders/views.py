from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cart.views import _get_cart
from catalog.models import Product
from .models import Order, OrderItem


def checkout(request):
    """
    Простое оформление заказа:
    - берём данные из формы (POST)
    - создаём Order и OrderItem из корзины
    """
    cart = _get_cart(request.session)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not (first_name and email):
            error = 'Имя и email обязательны'
            return render(
                request,
                'orders/checkout.html',
                {'error': error},
            )

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=first_name,
            email=email,
            phone=phone,
            address=address,
            comment=comment,
        )

        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {p.id: p for p in products}

        for product_id, data in cart.items():
            product = products_map.get(int(product_id))
            if not product:
                continue
            quantity = data.get('quantity', 1)
            price = product.get_price()
            OrderItem.objects.create(
                order=order,
                product=product,
                price=price,
                quantity=quantity,
            )

        # очистить корзину
        request.session['cart'] = {}
        request.session.modified = True

        return redirect(reverse('orders:thanks', kwargs={'order_id': order.id}))

    return render(request, 'orders/checkout.html')


def thanks(request, order_id: int):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/thanks.html', {'order': order})

