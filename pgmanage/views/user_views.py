# views/user_views.py

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from ..serializers.user_serializer import UserSerializer
from django.contrib.auth import authenticate


from django.contrib.auth import get_user_model

User = get_user_model()




@api_view(['POST'])
def register_owner(request):
    if request.method == 'POST':
        data = request.data
        # Make sure to assign 'owner' role to the new user
        data['role'] = 'owner'
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Owner registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register_tenant(request):
    if request.method == 'POST':
        data = request.data
        # Assign 'tenant' role to the new user
        data['role'] = 'tenant'
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Tenant registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_owner(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {"detail": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate the user
    user = authenticate(email=email, password=password)

    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "access": access_token,
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    

    
@api_view(['POST'])
def login_tenant(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {"detail": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authenticate the user
    user = authenticate(username=email, password=password)

    if user is not None:
        # Check if the user is a tenant (based on role)
        if user.role == 'tenant':
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    "access": access_token,
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "You are not authorized to log in as a tenant."},
                status=status.HTTP_403_FORBIDDEN
            )
    else:
        return Response(
            {"detail": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )    