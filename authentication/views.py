from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    user = get_user_model()

