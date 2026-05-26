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
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('footer_faq/', views.footer_faq, name='footer_faq'),
    path('about/', views.about, name='about'),

    path('mission/', views.mission, name='mission'),

    path('support-indian-artisans/',views.support_artisans,name='support_artisans'),

    path('customer-reviews/', views.reviews, name='reviews'),
    path('return-policy/',views.return_policy,name='return_policy'),

    path('shipping-info/',views.shipping_info,name='shipping_info'),

    path('payment-methods/',views.payment_methods,name='payment_methods'),

    path('help-center/',views.help_center,name='help_center'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)