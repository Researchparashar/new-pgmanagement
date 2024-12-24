from rest_framework import serializers
from ..models.tenantprofile import TenantProfile
from ..serializers.pg_serializer import PgSerializer
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()


class TenantProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    firstName = serializers.CharField(source="user.firstName", read_only=True)
    lastName = serializers.CharField(source="user.lastName", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)
    adharNumber = serializers.CharField(source="user.adharNumber", read_only=True)
    adharImage = serializers.ImageField(source="user.adharImage", read_only=True)
    # pg_details = PgSerializer(source="pg", read_only=True)
    secret = serializers.CharField(source="pg.secret", read_only=True)

    class Meta:
        model = TenantProfile
        fields = [
            "email",
            "firstName",
            "lastName",
            "role",
            "adharNumber",
            "adharImage",       
           
            "moveInDate",
            "moveOutDate",
            "roomNumber",
            "secret"
            
        ]
    def create(self, validated_data):
        # Handle creating TenantProfile, including roomNumber
        tenant_profile = TenantProfile.objects.create(**validated_data)
        return tenant_profile

   

    
  

