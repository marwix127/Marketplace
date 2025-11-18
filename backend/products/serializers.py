from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    class Meta:
        model = Product
        fields = ['id', 'owner', 'title', 'description', 'price', 'created_at', 'image']
        read_only_fields = ['id', 'owner', 'created_at']
