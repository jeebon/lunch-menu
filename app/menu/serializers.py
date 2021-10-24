from rest_framework import serializers

from core.models import Vote, Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for Restaurant objects"""

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'last_updated', 'created')
        read_only_fields = ('id', 'last_updated', 'created')


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for Vote objects"""

    class Meta:
        model = Vote
        fields = ('id', 'menu', 'user', 'date', 'last_updated', 'created')
        read_only_fields = ('id', 'last_updated', 'created')

class MenuSerializer(serializers.ModelSerializer):
    """Serialize a Menu"""
    
    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'name',
                  'items', 'date', 'winner', 'last_updated', 'created')
        read_only_fields = ('id', 'last_updated', 'created')

