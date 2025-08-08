# inventory/views.py
from rest_framework import viewsets
from .models import Product, Transaction, TransactionDetail
from .serializers import ProductSerializer, TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F, Q

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-transaction_date')
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['get'])
    def inventory(self, request):
        """
        Return current inventory per product: sum of IN quantities minus sum of OUT quantities.
        """
        # Sum quantity for IN transactions grouped by product
        ins = TransactionDetail.objects.filter(transaction__transaction_type='IN') \
            .values('product') \
            .annotate(total_in=Sum('quantity')) \
            .order_by()

        outs = TransactionDetail.objects.filter(transaction__transaction_type='OUT') \
            .values('product') \
            .annotate(total_out=Sum('quantity')) \
            .order_by()

        # convert to dict for fast lookup
        in_map = {i['product']: i['total_in'] for i in ins}
        out_map = {o['product']: o['total_out'] for o in outs}

        # build response for all products (even with zero)
        inventory_data = []
        from .models import Product
        for p in Product.objects.all().order_by('name'):
            q_in = in_map.get(p.id, 0) or 0
            q_out = out_map.get(p.id, 0) or 0
            balance = q_in - q_out
            inventory_data.append({
                'product_id': p.id,
                'product_name': p.name,
                'quantity': int(balance),
            })
        return Response(inventory_data)
