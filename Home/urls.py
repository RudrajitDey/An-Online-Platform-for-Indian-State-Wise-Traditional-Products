from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.Home, name="home"),
    path('state/<slug:slug>/', views.Home, name='home'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    path('become_seller/', views.become_seller, name="become_seller"),
    path('seller_login/', views.seller_login, name="seller_login"),
    path('vendor_dashboard/', views.vendor_dashboard, name="vendor_dashboard"),
    path('search/', views.search, name='search'),

    path('terms_condition/', views.terms_condition, name='terms_condition'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)