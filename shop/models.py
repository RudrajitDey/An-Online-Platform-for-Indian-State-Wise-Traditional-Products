from django.db import models
from django.conf import settings

# Create your models here.

class vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    shop_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)

    phone = models.CharField(max_length=15)
    email = models.EmailField()

    gst_number = models.CharField(max_length=20, unique=True)
    drug_license_number = models.CharField(max_length=50, unique=True)

    gst_certificate = models.FileField(upload_to='vendor_docs/gst/')
    drug_license_file = models.FileField(upload_to='vendor_docs/license/')
    id_proof = models.FileField(upload_to='vendor_docs/id/')

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name

