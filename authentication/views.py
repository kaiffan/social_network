from rest_framework.permissions import AllowAny, IsAuthenticated
from authentication.serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import status


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
            "first_name": serializer.data['first_name'],
            "last_name": serializer.data['last_name'],
            "email": serializer.data['email'],
            "birth_date": serializer.data['birth_date'],
            "reg_date": serializer.data['date_registration'],
        }
        return Response(response_data, status=status.HTTP_201_CREATED)  # изменить возврат


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        tokens = serializer.data.get("tokens")
        response_data = {
            "refresh_token": tokens.get('refresh'),
            "access_token": tokens.get('access')
        }
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
