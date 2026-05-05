from django.contrib import admin
from .models import State, Category, Product, faq

# Register your models here.

admin.site.register(State)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(faq)