from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from ..serializers.user_serializer import UserSerializer
from ..models.pg import PG
from ..models.tenantprofile import TenantProfile
from ..models import pg


from django.contrib.auth import get_user_model

User  = get_user_model()




@api_view(['GET'])
def tenant_profile(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        try:
            # Fetch the user's basic data
            user = User.objects.get(id=request.user.id)

            # Fetch the tenant profile
            tenant_profile = TenantProfile.objects.get(user=user)

            # Access the related PG instance
            pg = tenant_profile.pg  # This is the PG instance related to the tenant profile

            # Combine the data from both tables
            profile_data = {
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'role': user.role,
                'adharNumber': user.adhar_number,
                'adharImage': user.adhar_image.url if user.adhar_image else None,
                'moveInDate': tenant_profile.move_in_date,
                'moveOutDate': tenant_profile.move_out_date,
                'pg': tenant_profile.pg.name if tenant_profile.pg else None,
                'pgSecret': tenant_profile.pg.secret if tenant_profile.pg else None
            }

            return Response(profile_data)

        except User.DoesNotExist:
            return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except TenantProfile.DoesNotExist:
            return Response({"status": "error", "message": "Tenant profile not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"status": "error", "message": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tenant_profile(request):
    user = request.user
    data = request.data
    try:
        pg = PG.objects.get(secret=data.get("secret"))
        tenant_profile, created = TenantProfile.objects.get_or_create(user=user)
        tenant_profile.pg = pg
        tenant_profile.roomNumber = data.get("roomNumber")
        tenant_profile.moveInDate = data.get("moveInDate")
        tenant_profile.moveOutDate = data.get("moveOutDate")
        tenant_profile.save()

        return Response({"message": "Tenant profile updated successfully"}, status=status.HTTP_200_OK)
    except PG.DoesNotExist:
        return Response({"error": "Invalid PG secret"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tenant_details(request):
    if request.user.role != 'tenant':
        return Response({"error": "You are not authorized to view this data."}, status=status.HTTP_403_FORBIDDEN)

    # Fetch user details (basic)
    tenant = request.user
    user_serializer = UserSerializer(tenant)

    try:
        # Fetch tenant profile data
        tenant_profile = TenantProfile.objects.get(user=tenant)
        
        # Combine user data and tenant profile data
        combined_data = user_serializer.data
        combined_data.update({
            'moveInDate': tenant_profile.moveInDate,
            'moveOutDate': tenant_profile.moveOutDate,
            'roomNumber': tenant_profile.roomNumber,
            'pg': tenant_profile.pg.name if tenant_profile.pg else None  # Assuming PG has a name field
        })

        return Response(combined_data)

    except TenantProfile.DoesNotExist:
        return Response({"error": "Tenant profile not found."}, status=status.HTTP_404_NOT_FOUND)