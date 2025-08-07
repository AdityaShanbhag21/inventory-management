from django.contrib import admin
from .models import Product, Transaction, TransactionDetail

admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionDetail)
