from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def registration_user(request: Request) -> Response:
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_data = {
        "first_name": serializer.data['first_name'],
        "last_name": serializer.data['last_name'],
        "email": serializer.data['email'],
        "birth_date": serializer.data['birth_date'],
        "registration_date": serializer.data['registration_date']
    }
    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def registration_user(request: Request) -> Response:
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    tokens = serializer.data.get("tokens")
    response_data = {
        "refresh_token": tokens.get('refresh'),
        "access_token": tokens.get('access')
    }
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def registration_user(request: Request) -> Response:
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(status=status.HTTP_204_NO_CONTENT)
