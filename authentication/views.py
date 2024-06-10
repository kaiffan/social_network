from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[AllowAny, ])
def registration_user(request: Request) -> Response:
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[AllowAny, ])
def login_user(request: Request) -> Response:
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    current_user = serializer.validated_data
    return Response(
        data={
            "theme": current_user.theme,
            "refresh_token": current_user.tokens.get('refresh'),
            "access_token": current_user.tokens.get('access')
        }, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def logout_user(request: Request) -> Response:
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def get_user_id(request: Request) -> Response:
    return Response(data=request.user.id, status=status.HTTP_200_OK)
