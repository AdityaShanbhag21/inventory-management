# inventory/serializers.py
from rest_framework import serializers
from .models import Product, Transaction, TransactionDetail
from django.utils import timezone
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit_price', 'created_at']

class TransactionDetailSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = TransactionDetail
        fields = ['id', 'product', 'quantity', 'unit_price', 'total']
        read_only_fields = ['total']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Unit price cannot be negative.")
        return value

    def create(self, validated_data):
        # total will be computed in model.save()
        detail = TransactionDetail(**validated_data)
        detail.save()
        return detail

class TransactionSerializer(serializers.ModelSerializer):
    transaction_details = TransactionDetailSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type', 'transaction_date', 'transaction_details', 'created_at']

    def validate_transaction_date(self, value):
        # Optional: prevent far future dates
        if value > timezone.now() + timezone.timedelta(days=365):
            raise serializers.ValidationError("Transaction date seems too far in the future.")
        return value

    def create(self, validated_data):
        details_data = validated_data.pop('transaction_details')
        transaction = Transaction.objects.create(**validated_data)
        for d in details_data:
            # attach transaction reference
            TransactionDetail.objects.create(transaction=transaction, **d)
        return transaction
