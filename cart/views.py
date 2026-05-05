from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from Home.models import Product

from django.contrib.auth.decorators import login_required



# Create your views here.

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.session_key

        if not cart_id:
            cart_id = request.session.create()

        cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    return cart

def merge_cart(request, user):
    session_cart_id = request.session.session_key

    if session_cart_id:
        try:
            session_cart = Cart.objects.get(cart_id=session_cart_id)
            user_cart, created = Cart.objects.get_or_create(user=user)

            items = CartItem.objects.filter(cart=session_cart)

            for item in items:
                existing_item = CartItem.objects.filter(
                    cart=user_cart,
                    product=item.product
                ).first()

                if existing_item:
                    existing_item.quantity += item.quantity
                    existing_item.save()
                else:
                    item.cart = user_cart
                    item.save()

            session_cart.delete()

        except Cart.DoesNotExist:
            pass





def add_to_cart(request, product_id, product_type):
    cart = _get_cart(request)

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart')



def cart_view(request):
    cart = _get_cart(request)
    items = cart.items.all()

    total = sum(item.total_price() for item in items)
    tax = (5 * total) / 100
    grand_total = total + tax

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    })


def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
    cart = _get_cart(request)
    items = cart.items.all()
    total = sum(item.total_price() for item in items)
    tax = (5 * total)/100
    grand_total = total + tax
    
    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'items': items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total
    })
