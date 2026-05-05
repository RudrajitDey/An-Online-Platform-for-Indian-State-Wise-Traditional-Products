from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Order, OrderProduct, Payment
from cart.views import _get_cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import json

# Create your views here.

def validate_cart_stock(cart_items):
    for item in cart_items:
        product = item.get_product()
        if product.stock < item.quantity:
            return False, f'Insufficient stock for {product.product_name}. Available: {product.stock}, Requested: {item.quantity}'
    return True, None



@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        cart = _get_cart(request)
        items = cart.items.all()
        
        if not items.exists():
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')
        
        # Validate stock availability before processing
        stock_valid, stock_error = validate_cart_stock(items)
        if not stock_valid:
            messages.error(request, stock_error)
            return redirect('cart')
        
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        country = request.POST.get('country', 'India')
        payment_method = request.POST.get('payment_method', 'cod')
        
        # Create order
        import uuid
        order_number = str(uuid.uuid4())[:8].upper()
        
        total = sum(item.total_price() for item in items)
        tax = (5 * total) / 100
        
        # Get user IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            pin_code=pincode,
            country=country,
            order_total=total,
            tax=tax,
            status='New',
            is_ordered=True,
            ip=ip
        )
        
        # Create order items and reduce stock
        for item in items:
            product = item.get_product()

            # ✅ Stock validation (already done before, but double safety)
            if product and hasattr(product, 'stock'):
                if product.stock < item.quantity:
                    messages.error(
                        request,
                        f'Insufficient stock for {product.product_name}. Available: {product.stock}, Requested: {item.quantity}'
                    )
                    return redirect('cart')

            # ✅ Create OrderProduct (simple)
            OrderProduct.objects.create(
                order=order,
                user=request.user,
                product=product,
                quantity=item.quantity,
                product_price=product.price if product else 0,
                ordered=True
            )

            # Reduce stock
            if product and hasattr(product, 'stock'):
                product.stock -= item.quantity
                product.save()
        
        # Clear cart
        items.delete()
        cart.delete()
        
        return redirect('payments')
    
    return redirect('checkout')

@login_required(login_url='login')
def order_confirmation(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = OrderProduct.objects.filter(order=order)
        
        context = {
            'order': order,
            'order_items': order_items,
            'total': order.order_total + order.tax
        }
        return render(request, 'orders/order_confirmation.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found!')
        return redirect('home')
    

@login_required(login_url='login')
def payments(request):
    
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            payment = Payment()
            payment_method = body.get('payment_method')
        except json.JSONDecodeError:
            payment_method = request.POST.get('payment_method')
        
        # Get the most recent order for this user
        try:
            order = Order.objects.filter(user=request.user).order_by('-created_at').first()
            if not order:
                messages.error(request, 'No order found!')
                return redirect('home')
            
            # Create payment record
            import uuid
            payment_id = str(uuid.uuid4())[:12].upper()
            
            payment = Payment.objects.create(
                user=request.user,
                payment_id=payment_id,
                payment_method=payment_method,
                amount_paid=str(order.order_total + order.tax),
                status='Completed'  # In real app, this would be 'Pending' initially
            )
            
            # Update order with payment reference
            order.payment = payment
            order.status = 'Accepted'
            order.is_ordered = True
            order.save()
            
            # Handle different payment methods
            if payment_method == 'cod':
                messages.success(request, 'Order placed successfully! Pay on delivery.')
            elif payment_method == 'card':
                # In real app, integrate with payment gateway
                messages.success(request, 'Payment successful! Order confirmed.')
            elif payment_method == 'upi':
                # In real app, redirect to UPI app
                messages.success(request, 'UPI payment initiated! Order confirmed.')
            elif payment_method == 'netbanking':
                # In real app, redirect to bank portal
                messages.success(request, 'Net banking payment initiated! Order confirmed.')
            
            # Return JSON response for PayPal redirect
            return JsonResponse({
                'success': True,
                'redirect_url': f'/orders/order_confirmation/{order.id}/'
            })
            
        except Exception as e:
            messages.error(request, f'Payment processing failed: {str(e)}')
            return redirect('payments')
    
    # GET request - show payment page with order details
    try:
        # Get the most recent order for this user (regardless of status)
        order = Order.objects.filter(user=request.user).order_by('-created_at').first()
        if order:
            order_items = OrderProduct.objects.filter(order=order)
            total = order.order_total + order.tax
        else:
            order = None
            order_items = []
            total = 0
    except:
        order = None
        order_items = []
        total = 0
    
    context = {
        'order': order,
        'order_items': order_items,
        'total': total
    }
    return render(request, 'orders/payments.html', context)





