from django.contrib.auth.models import User
from django.db import models
from event.models import Event


class OrderStatus(models.Model):
    status = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.status


class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("refunded", "Refunded"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    establishment_fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
