from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers.pg_serializer import PgSerializer
from ..models.pg import PG # Make sure the model is imported
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
def addpg(request):
    if request.method == 'POST':
        # Ensure that only logged-in users (owners) can add a PG
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Ensure the logged-in user is the owner
        data = request.data
        data['owner'] = request.user.id  # Automatically set the logged-in user as the owner
        
        serializer = PgSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            print(f"Response data: {serializer.data}") 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
