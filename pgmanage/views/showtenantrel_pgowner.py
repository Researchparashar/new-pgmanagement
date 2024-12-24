from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from ..models.pg import PG
from rest_framework import status
from django.contrib.auth import get_user_model
from ..models.tenantprofile import TenantProfile
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def owner_view_tenants(request):
    

#     # Check if the user is an owner
#     if request.user.role != 'owner':
#         return Response({"error": "You are not authorized to view this data."}, status=status.HTTP_403_FORBIDDEN)

#     # Fetch the PGs owned by the authenticated owner
#     owner = request.user
#     try:
#         # Get all PGs that belong to the owner
#         pgs = PG.objects.filter(owner=owner)

#         tenant_data = []
        
#         # Loop through each PG and fetch the tenants
#         for pg in pgs:
#             tenants = TenantProfile.objects.filter(pg=pg)
            
#             for tenant in tenants:
#                 tenant_info = {
#                     'firstName': tenant.user.firstName,
#                     'lastName': tenant.user.lastName,
#                     'email': tenant.user.email,
#                     'roomNumber': tenant.roomNumber,
#                     'moveInDate': tenant.moveInDate,
#                     'moveOutDate': tenant.moveOutDate,
#                     'adharNumber': tenant.user.adharNumber,
#                     'adharImage': tenant.user.adharImage.url if tenant.user.adharImage else None,
#                     'pgName': pg.name,
#                     'pgSecret': pg.secret
#                 }
#                 tenant_data.append(tenant_info)

#         if not tenant_data:
#             return Response({"message": "No tenants found."}, status=status.HTTP_404_NOT_FOUND)

#         return Response({"tenants": tenant_data}, status=status.HTTP_200_OK)

#     except PG.DoesNotExist:
#         return Response({"error": "No PG found for the authenticated owner."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def owner_view_tenants(request, pg_secret):
    # Check if the user is an owner
    if request.user.role != 'owner':
        return Response({"error": "You are not authorized to view this data."}, status=status.HTTP_403_FORBIDDEN)

    try:
        # Fetch the specific PG owned by the authenticated owner
        pg = PG.objects.get(secret=pg_secret, owner=request.user)

        # Fetch tenants for the specific PG
        tenants = TenantProfile.objects.filter(pg=pg)

        tenant_data = []

        for tenant in tenants:
            tenant_info = {
                'firstName': tenant.user.firstName,
                'lastName': tenant.user.lastName,
                'email': tenant.user.email,
                'roomNumber': tenant.roomNumber,
                'moveInDate': tenant.moveInDate,
                'moveOutDate': tenant.moveOutDate,
                'adharNumber': tenant.user.adharNumber,
                'adharImage': tenant.user.adharImage.url if tenant.user.adharImage else None,
                'contact':tenant.contact
            }
            tenant_data.append(tenant_info)

        # If no tenants are found
        if not tenant_data:
            return Response({"message": "No tenants found for this PG."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "pgName": pg.name,
            "pgSecret": pg.secret,
            "tenants": tenant_data
        }, status=status.HTTP_200_OK)

    except PG.DoesNotExist:
        return Response({"error": "PG not found or you do not own this PG."}, status=status.HTTP_404_NOT_FOUND)

