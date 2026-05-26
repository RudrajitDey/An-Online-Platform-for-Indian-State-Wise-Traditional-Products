"""
URL configuration for Indian_Traditional_Shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/settings/#

For the full list of settings and their values, see
    https://docs.djangoproject.com/en/5.2/ref/settings/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Home import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('cart/', include('cart.urls')),
    path('shop/', include('shop.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
]

# Error handlers
handler404 = home_views.error_404
handler500 = home_views.error_500
handler400 = home_views.error_400

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
