
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models.pg import PG
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET'])
    
def show_pgs_owner(request):
    if request.user.role != 'owner':
        raise PermissionDenied("You are not authorized to view this data.")
    
    # Get the PGs belonging to the logged-in owner
    owner = request.user
    pgs = PG.objects.filter(owner=owner)
    
    # Serialize the PG data to return in the response
    pg_data = [
        {
            'id': pg.id,
            'name': pg.name,
            'address': pg.address,
            'owner': pg.owner.id,
            'secret':pg.secret
        } for pg in pgs
    ]
    
    return Response(pg_data, status=status.HTTP_200_OK)