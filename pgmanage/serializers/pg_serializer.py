from rest_framework import serializers
from ..models.pg import PG
from django.contrib.auth import get_user_model

User = get_user_model()


class PgSerializer(serializers.ModelSerializer):
    # Ensure 'owner' is a valid User object, and it's passed correctly in the serializer
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = PG
        fields = ['secret','name', 'address', 'owner','id']
        read_only_fields = ['secret'] 

    def create(self, validated_data):
        # Ensure that 'owner' is properly passed to the model
        owner = validated_data.get('owner')
        name = validated_data.get('name')
        address = validated_data.get('address')
       
      
        
        # Create PG object with owner and other validated data
        pg_instance = PG.objects.create(owner=owner, name=name, address=address)
        return pg_instance
