from rest_framework import serializers
from .models import Product, Transaction, TransactionDetail

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit_price', 'created_at']

class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = ['id', 'transaction', 'product', 'quantity', 'unit_price', 'total']

class TransactionSerializer(serializers.ModelSerializer):
    transaction_details = TransactionDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'transaction_date', 'transaction_details', 'created_at']

    def create(self, validated_data):
        transaction_details_data = validated_data.pop('transaction_details')
        transaction = Transaction.objects.create(**validated_data)
        for detail in transaction_details_data:
            TransactionDetail.objects.create(transaction=transaction, **detail)
        return transaction
