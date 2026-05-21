from django.shortcuts import render, get_object_or_404

from .models import State, Category, Product, faq


from django.shortcuts import render, redirect
from accounts.models import Account
from shop.models import vendor
from django.contrib import messages
from django.db.models import Q
from django.contrib import auth


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
        try:
            # Validate required fields
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            shop_name = request.POST.get('shop_name', '').strip()
            owner_name = request.POST.get('owner_name', '').strip()
            phone = request.POST.get('phone', '').strip()
            
            # Basic validation
            if not username or not email or not password or not shop_name:
                messages.error(request, "Please fill in all required fields (Username, Email, Password, Shop Name)")
                return render(request, 'footer/become_seller.html')
            
            # Check if username already exists
            if Account.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return render(request, 'footer/become_seller.html')
            
            # Check if email already exists
            if Account.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
                return render(request, 'footer/become_seller.html')
            
            # Create user
            user = Account.objects.create_user(
                first_name=owner_name,
                last_name='',
                username=username,
                email=email,
                password=password
            )

            # Create vendor record
            vendor.objects.create(
                user=user,
                shop_name=shop_name,
                owner_name=owner_name,
                phone=phone,
                email=email,
                gst_number=request.POST.get('gst', ''),
                drug_license_number=request.POST.get('license', ''),
                gst_certificate=request.FILES.get('gst_file'),
                drug_license_file=request.FILES.get('license_file'),
                id_proof=request.FILES.get('id_proof'),
                city=request.POST.get('city', ''),
                status='pending',
                is_active=False
            )

            messages.success(request, "Seller registration successful! Wait for admin approval.")
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return render(request, 'footer/become_seller.html')

    return render(request, 'footer/become_seller.html')

from django.contrib.auth import authenticate, login
from accounts.models import Account


def seller_login(request):

    if request.method == "POST":

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            return render(
                request,
                'authentication/login.html',
                {
                    'error': 'Please enter both username and password'
                }
            )

        try:
            # Find account using username
            account = Account.objects.get(username=username)

            # IMPORTANT: authenticate using EMAIL
            user = auth.authenticate(
                request,
                email=account.email,
                password=password
            )

            if user is not None:

                try:
                    vendor_obj = vendor.objects.get(user=user)

                    if vendor_obj.is_active:

                        # Proper Django login
                        auth.login(request, user)

                        messages.success(
                            request,
                            f"Welcome back, {vendor_obj.shop_name}!"
                        )

                        return redirect('vendor_dashboard')

                    else:
                        messages.error(
                            request,
                            'Your seller account is pending approval.'
                        )

                except vendor.DoesNotExist:
                    messages.error(
                        request,
                        'No vendor account found.'
                    )

            else:
                messages.error(
                    request,
                    'Invalid username or password'
                )

        except Account.DoesNotExist:
            messages.error(
                request,
                'Invalid username or password'
            )

    return render(request, 'authentacition/login.html')

# def vendor_dashboard(request):

#     return render(request, 'vendor_dashboard/vendor_dashboard.html')


from django.contrib.auth.decorators import login_required
from django.db.models import Sum
 


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

