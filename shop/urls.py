from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("seller_list/", views.seller_list, name="seller_list"),
    path('approve_vendor/<int:id>/', views.approve_vendor, name='approve_vendor'),
    path('reject_vendor/<int:id>/', views.reject_vendor, name='reject_vendor'),
    path('delete_vendor/<int:id>/', views.delete_vendor, name='delete_vendor'),
    path('seller_product_list', views.seller_product_list, name="seller_product_list"),
    path('approve_product/<int:id>/', views.approve_product, name='approve_product'),
    path('reject_product/<int:id>/', views.reject_product, name='reject_product'),
    path('orders_list', views.orders_list, name="orders_list"),

    path('orders_list/<int:order_id>/',views.order_view,name='order_view'),

    path('orders_list/delete/<int:order_id>/',views.order_delete,name='order_delete'),

    path("earnings/", views.earnings, name="earnings"),

    path('product_page/', views.product_page, name="product_page"),
    path('add_product/', views.add_product, name="add_product"),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),

    path('all_products/', views.all_products, name="all_products"),
    path('all_orders/', views.all_orders, name="all_orders"),
]   


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
