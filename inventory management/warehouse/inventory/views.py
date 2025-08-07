from django.shortcuts import render

from rest_framework import viewsets
from .models import Product, Transaction
from .serializers import ProductSerializer, TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['get'])
    def inventory(self, request):
        products = Product.objects.all()
        inventory_data = []
        for product in products:
            stock_in = Transaction.objects.filter(transactiondetail__product=product, transaction_type='IN').aggregate(Sum('transactiondetail__quantity'))['transactiondetail__quantity__sum'] or 0
            stock_out = Transaction.objects.filter(transactiondetail__product=product, transaction_type='OUT').aggregate(Sum('transactiondetail__quantity'))['transactiondetail__quantity__sum'] or 0
            stock_balance = stock_in - stock_out
            inventory_data.append({
                'product': product.name,
                'quantity': stock_balance
            })
        return Response(inventory_data)

