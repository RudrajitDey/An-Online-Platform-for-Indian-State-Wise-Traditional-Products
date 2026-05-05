from django.shortcuts import render, get_object_or_404

from .models import State, Category, Product, faq


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from shop.models import vendor
from django.contrib import messages
from django.db.models import Q

# Create your views here.

def Home(request):

    states = State.objects.prefetch_related('categories')
    faqs = faq.objects.all()

    return render(request, 'home.html', {
       'states': states,
        'faqs': faqs,               
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()

    return render(request, 'products/category_products.html', {
        'subcategory': category,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:8]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


def become_seller(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )

        vendor.objects.create(
            user=user,
            shop_name=request.POST['shop_name'],
            owner_name=request.POST['owner_name'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            gst_number=request.POST['gst'],
            drug_license_number=request.POST['license'],
            gst_certificate=request.FILES.get('gst_file'),
            drug_license_file=request.FILES.get('license_file'),
            id_proof=request.FILES.get('id_proof'),
            city=request.POST['city'],
            status='pending',
            is_active=False
        )

        messages.success(request, "Request sent! Wait for admin approval.")
        return redirect('Home')

    return render(request, 'footer/become_seller.html')

from django.contrib.auth import authenticate, login


def seller_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            try:
                vendors = vendor.objects.get(user=user)

                if vendor.is_active:
                    login(request, user)
                    return redirect('vendor_dashboard')
                else:
                    return render(request, 'authentication/login.html', {
                        'error': 'Wait for admin approval'
                    })

            except vendor.DoesNotExist:
                return render(request, 'authentication/login.html', {
                    'error': 'Not a vendor account'
                })

        else:
            return render(request, 'authentication/login.html', {
                'error': 'Invalid credentials'
            })

    return render(request, 'authentication/login.html')

# def vendor_dashboard(request):

#     return render(request, 'vendor_dashboard/vendor_dashboard.html')


from django.contrib.auth.decorators import login_required
from django.db.models import Sum
 

@login_required
def vendor_dashboard(request):
    
    
    if not hasattr(request.user, 'vendor'):
        return redirect('seller_login')

    vendor = request.user.vendor

    
    total_products = Product.objects.filter(vendor=vendor).count()

    context = {
        'vendor': vendor,
        'total_products': total_products,

    }

    return render(request, 'vendor_dashboard/vendor_dashboard.html', context)

def search(request):
    query = request.GET.get('q')
    results = []
    total_results = 0

    if query:
        # Search in multiple fields for better results
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query) |
            Q(state__name__icontains=query)
        ).filter(is_available=True, status='approved').distinct()
        
        total_results = results.count()

    return render(request, 'products/search_results.html', {
        'query': query,
        'results': results,
        'total_results': total_results,
    })

