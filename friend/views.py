from friend.serializers import FriendUpdateFieldSerializer, FriendSerializer, FriendAddSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from friend.models import Friend
from authentication.models import CustomUser


@api_view(http_method_names=['DELETE'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def delete_friend(request: Request, friend_id: int) -> Response:
    try:
        friend = Friend.objects.filter(friend_id=friend_id).filter(user_id=request.user.id).first()
    except Friend.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        friend.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PATCH'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def update_status_friend(request: Request, friend_id: int) -> Response:
    try:
        friend = Friend.objects.filter(friend_id=friend_id).filter(user_id=request.user.id).first()
    except Friend.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = FriendUpdateFieldSerializer(instance=friend, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def get_all_friends_user(request: Request) -> Response:
    try:
        friends = Friend.objects.filter(user_id=request.user.id).filter(status="ACCEPTED").all()
    except Friend.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = FriendSerializer(
            friends,
            many=True
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def add_friend(request: Request, friend_id: int) -> Response:
    try:
        CustomUser.objects.get(id=friend_id)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        friend = Friend(friend_id=friend_id, user_id=request.user.id)
        friend.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
