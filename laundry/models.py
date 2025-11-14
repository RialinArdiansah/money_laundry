from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
    ROLE_CHOICES = (
        ('EMPLOYEE', 'Pegawai'),
        ('OWNER', 'Owner'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    position = models.CharField(max_length=100, blank=True)


class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    SERVICE_CHOICES = (
        ('EXPRESS', 'Express'),
        ('REGULAR', 'Regular'),
    )
    STATUS_CHOICES = (
        ('DITERIMA', 'Diterima'),
        ('PROSES', 'Proses'),
        ('SELESAI', 'Selesai'),
        ('SIAP_DIAMBIL', 'Siap Diambil'),
    )
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_in = models.DateField(default=timezone.now)
    estimated_done = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DITERIMA')
    storage_deadline = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = 'ML' + uuid.uuid4().hex[:10].upper()
        if not self.total_cost:
            price_per_kg = 10000 if self.service_type == 'REGULAR' else 15000
            self.total_cost = price_per_kg * float(self.weight_kg)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number