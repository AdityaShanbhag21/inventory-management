# inventory/models.py
from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'IN'),
        ('OUT', 'OUT'),
    )
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=3)
    transaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} @ {self.transaction_date.isoformat()}"

class TransactionDetail(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='transaction_details')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='transaction_details')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])  # quantity must be >= 1
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        # Ensure total is consistent; derive if missing or incorrect
        calculated = self.quantity * self.unit_price
        # Allow small rounding difference; but force consistency
        self.total = calculated
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} x {self.quantity} ({self.transaction.transaction_type})"
