from django.db import models
from django.utils.text import slugify

from shop.models import vendor

# Create your models here.

# State_Model
class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to="states/")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

# State_Wise_category_Model
class Category(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="categories/")
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1

            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
       
    def __str__(self):
        return self.name
    

class Product(models.Model):
    vendor = models.ForeignKey(vendor, on_delete = models.CASCADE, blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(default=0)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    expiry_date = models.DateField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    rating = models.FloatField(default=0, blank=True, null=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductContent(models.Model):
    SECTION_CHOICES = [
        ('uses', 'Uses'),
        ('dosage', 'Dosage'),
        ('side_effects', 'Side Effects'),
        ('warnings', 'Warnings'),
        ('precautions', 'Precautions'),
        ('interactions', 'Interactions'),
        ('storage', 'Storage'),
        ('quick_tips', 'Quick Tips'),
        ('faq', 'FAQs'),
        ('lifestyle', 'Lifestyle Recommendation'),
    ]

    product_s = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='contents')
    section_type = models.CharField(max_length=50, choices=SECTION_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.product_s.name} - {self.section_type}"
    


class ProductPoint(models.Model):
    content = models.ForeignKey(ProductContent, on_delete=models.CASCADE, related_name='points')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


# FAQS Model
class faq(models.Model):
    faq_question = models.CharField(max_length=300)
    faq_answer = models.TextField(blank=True)

    def __str__(self):
        return self.faq_question
    
    


