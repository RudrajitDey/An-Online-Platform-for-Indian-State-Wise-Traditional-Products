from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import vendor
from Home.models import Product, ProductContent, ProductPoint
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from accounts.models import Account
from orders.models import OrderProduct, Order
from django.db.models import Count, Sum, Avg
from django.db import models

from django.utils import timezone
from datetime import timedelta

# Create your views here.

def admin_dashboard(request):


     # Get total counts
    total_users = Account.objects.count()
    total_vendors = vendor.objects.count()
    total_orders = Order.objects.count()
    
    # Get recent orders with items
    recent_orders = Order.objects.select_related('user').prefetch_related('order_items').order_by('-created_at')[:10]
    
    # Get best selling products (simplified query)
    best_selling_products = Product.objects.filter(
        orderproduct__isnull=False
    ).distinct().order_by('-created_at')[:10]
    
    # Calculate total earnings
    total_earnings = OrderProduct.objects.aggregate(
        total=Sum('product_price')
    )['total'] or 0
    
    # Calculate growth percentages (simplified - you may want to implement actual period comparison)
    user_growth_percentage = 12.5  # Example percentage
    order_growth_percentage = 8.2   # Example percentage  
    vendor_growth_percentage = 15.3 # Example percentage
    earnings_growth_percentage = 22.1 # Example percentage
    
    context = {
        'total_users': total_users,
        'total_vendors': total_vendors,
        'total_orders': total_orders,
        'total_earnings': f"{total_earnings:.2f}",
        'user_growth_percentage': user_growth_percentage,
        'order_growth_percentage': order_growth_percentage,
        'vendor_growth_percentage': vendor_growth_percentage,
        'earnings_growth_percentage': earnings_growth_percentage,
        'recent_orders': recent_orders,
        'best_selling_products': best_selling_products,
    }

    return render(request, 'admin/admin_dashboard.html', context)

def seller_list(request):

    vendors = vendor.objects.all().order_by('-created_at')

    return render(request, 'admin/seller/seller_list.html', {'vendors': vendors})

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404


def approve_vendor(request, id):
    v = get_object_or_404(vendor, id=id)

    v.status = 'approved'
    v.is_active = True
    v.save()

    # 📧 Send Email
    send_mail(
        subject="Seller Approved ✅",
        message=f"""
Hello {v.owner_name},

Your seller account has been approved 🎉

You can now login and start selling.

Thank you!
""",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[v.email],
        fail_silently=False
    )

    return redirect('seller_list')

def reject_vendor(request, id):
    v = get_object_or_404(vendor, id=id)

    v.status = 'rejected'
    v.is_active = False
    v.save()

    send_mail(
        subject="Seller Rejected ❌",
        message="Your seller request was rejected. Contact support.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[v.email],
        fail_silently=True
    )

    return redirect('seller_list')

def delete_vendor(request, id):
    v = get_object_or_404(vendor, id=id)
    user = v.user
    v.delete()
    user.delete()
    return redirect('seller_list')


def seller_product_list(request):

    vendors = vendor.objects.all().order_by('-created_at')
    seller_products = Product.objects.all()
    
    return render(request, 'admin/seller/seller_product_list.html', {'seller_products': seller_products, 'vendors': vendors})

def approve_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.status = 'approved'
    product.save()
    return redirect('seller_product_list')


def reject_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.status = 'rejected'
    product.save()
    return redirect('seller_product_list')


from django.db.models import Q, Sum, Count
from datetime import datetime



def orders_list(request):

    # =========================================
    # BASE QUERY
    # =========================================

    orders = (
        Order.objects
        .select_related('user', 'payment')
        .prefetch_related('order_items__product')
        .annotate(
            total_items=Count('order_items'),
            total_quantity=Sum('order_items__quantity')
        )
        .order_by('-created_at')
    )




    # =========================================
    # DASHBOARD STATS
    # =========================================

    total_orders = orders.count()

    total_revenue = (
        orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    new_orders = orders.filter(status='New').count()

    completed_orders = orders.filter(status='Completed').count()

    cancelled_orders = orders.filter(status='Cancelled').count()



    # =========================================
    # RECENT ORDERS
    # =========================================

    recent_orders = orders[:10]



    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'orders': orders,

        # stats
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'new_orders': new_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,

    
        # recent
        'recent_orders': recent_orders,

    }

    return render(
        request,
        'admin/orders/orders_list.html',
        context
    )

def order_view(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related('order_items__product'),
        id=order_id
    )

    return render(
        request,
        'admin/orders/orders_list_view.html',
        {
            'order': order
        }
    )


def order_delete(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    order.delete()

    messages.success(request, 'Order deleted successfully.')

    return redirect('orders_list')




def earnings(request):

    # =========================
    # ALL ORDERS
    # =========================
    all_orders = Order.objects.all()

    # =========================
    # TOTAL EARNINGS
    # =========================
    total_earnings = (
        all_orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    # =========================
    # COMPLETED ORDERS
    # =========================
    completed_orders = all_orders.filter(
        status='Completed'
    )

    completed_earnings = (
        completed_orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    # =========================
    # NEW / PENDING ORDERS
    # =========================
    pending_orders = all_orders.filter(
        status='New'
    )

    pending_earnings = (
        pending_orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    # =========================
    # ACCEPTED ORDERS
    # =========================
    accepted_orders = all_orders.filter(
        status='Accepted'
    )

    accepted_earnings = (
        accepted_orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    # =========================
    # CANCELLED ORDERS
    # =========================
    cancelled_orders = all_orders.filter(
        status='Cancelled'
    )

    cancelled_earnings = (
        cancelled_orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    # =========================
    # MONTHLY EARNINGS
    # =========================
    current_month = timezone.now().replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    monthly_orders = all_orders.filter(
        created_at__gte=current_month
    )

    monthly_earnings = (
        monthly_orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    # =========================
    # TODAY EARNINGS
    # =========================
    today = timezone.now().date()

    today_orders = all_orders.filter(
        created_at__date=today
    )

    today_earnings = (
        today_orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    # =========================
    # LAST 7 DAYS EARNINGS
    # =========================
    last_7_days = timezone.now() - timedelta(days=7)

    weekly_orders = all_orders.filter(
        created_at__gte=last_7_days
    )

    weekly_earnings = (
        weekly_orders.aggregate(
            total=Sum('order_total')
        )['total'] or 0
    )

    # =========================
    # TOTAL TAX
    # =========================
    total_tax = (
        all_orders.aggregate(
            total=Sum('tax')
        )['total'] or 0
    )

    # =========================
    # AVERAGE ORDER VALUE
    # =========================
    total_orders_count = all_orders.count()

    if total_orders_count > 0:
        average_order_value = total_earnings / total_orders_count
    else:
        average_order_value = 0

    # =========================
    # RECENT ORDERS
    # =========================
    recent_orders = all_orders.order_by(
        '-created_at'
    )[:10]

    # =========================
    # CONTEXT
    # =========================
    context = {

        # Earnings
        'total_earnings': total_earnings,
        'completed_earnings': completed_earnings,
        'pending_earnings': pending_earnings,
        'accepted_earnings': accepted_earnings,
        'cancelled_earnings': cancelled_earnings,

        # Time Based
        'monthly_earnings': monthly_earnings,
        'today_earnings': today_earnings,
        'weekly_earnings': weekly_earnings,

        # Other Stats
        'total_tax': total_tax,
        'average_order_value': round(average_order_value, 2),

        # Counts
        'total_orders_count': total_orders_count,
        'completed_orders_count': completed_orders.count(),
        'pending_orders_count': pending_orders.count(),
        'accepted_orders_count': accepted_orders.count(),
        'cancelled_orders_count': cancelled_orders.count(),

        # Recent Orders
        'recent_orders': recent_orders,
    }

    return render(
        request,
        'admin/earnings/earnings.html',
        context
    )


def product_page(request):
    vendor = request.user.vendor
    seller_product = Product.objects.filter(vendor=vendor)
    return render(request, 'vendor_dashboard/seller_pages/product_page.html', {'seller_product':seller_product})

@login_required
def add_product(request):
    try:
        vendor_obj = vendor.objects.get(user=request.user)
    except vendor.DoesNotExist:
        return render(request, 'vendor_dashboard/seller_pages/add_product.html', {
            'error': 'You are not registered as a vendor'
        })

    # ❗ Prevent unapproved sellers
    if vendor_obj.status != 'approved':
        return render(request, 'vendor_dashboard/seller_pages/add_product.html', {
            'error': 'Wait for admin approval before adding products'
        })

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        brand = request.POST.get('brand')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        expiry_date = request.POST.get('expiry_date')
        image = request.FILES.get('image')
        discount_price = request.POST.get('discount_price')
        is_available=True if request.POST.get('is_available') == "True" else False

        product = Product.objects.create(
            vendor=vendor_obj,
            name=name,
            slug=slugify(name),
            description=description,
            category=category,
            brand=brand,
            price=price,
            stock=stock,
            expiry_date=expiry_date,
            image=image,
            discount_price=discount_price,
            is_available=is_available
        )



        # 👉 Handle dynamic sections
        section_types = request.POST.getlist('section_type[]')
        titles = request.POST.getlist('section_title[]')
        contents = request.POST.getlist('section_content[]')

        for i in range(len(section_types)):
            if contents[i]:  # avoid empty
                content_obj = ProductContent.objects.create(
                    product_s=product,
                    section_type=section_types[i],
                    title=titles[i],
                    content=contents[i]
                )

                # 👉 Convert lines to bullet points
                lines = contents[i].split("\n")
                for line in lines:
                    if line.strip():
                        ProductPoint.objects.create(
                            content=content_obj,
                            text=line.strip()
                        )

        messages.success(request, "Product added successfully ✅")
        return redirect('add_product')  # reload page

    return render(request, 'vendor_dashboard/seller_pages/add_product.html')

# Edit Product

@login_required
def edit_product(request, id):
    vendor_obj = get_object_or_404(vendor, user=request.user)
    product = get_object_or_404(Product, id=id, vendor=vendor_obj)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.category = request.POST.get('category')
        product.brand = request.POST.get('brand')
        product.price = request.POST.get('price')
        product.discount_price = request.POST.get('discount_price')
        product.stock = request.POST.get('stock')
        product.expiry_date = request.POST.get('expiry_date')

        # Boolean fix
        product.is_available = True if request.POST.get('is_available') == "True" else False

        # Image update (optional)
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        messages.success(request, "Product updated successfully ✅")
        return redirect('product_page')

    return render(request, 'vendor_dashboard/seller_pages/edit_product.html', {
        'product': product
    })

# Delete Product

@login_required
def delete_product(request, id):
    vendor_obj = get_object_or_404(vendor, user=request.user)
    product = get_object_or_404(Product, id=id, vendor=vendor_obj)

    product.delete()
    messages.success(request, "Product deleted successfully ❌")
    return redirect('product_page')