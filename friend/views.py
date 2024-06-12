from friend.serializers import FriendSerializer
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
        friend_user = Friend.objects.filter(friend_id=friend_id).filter(user_id=request.user.id).filter(
            status="ACCEPTED").first()
        user_friend = Friend.objects.filter(friend_id=request.user.id).filter(user_id=friend_id).filter(
            status="ACCEPTED").first()
    except Friend.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        friend_user.delete()
        user_friend.delete()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def get_all_friends_user(request: Request) -> Response:
    try:
        friends = Friend.objects.filter(user_id=request.user.id).all()
    except Friend.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":  # user_id кто отправил запрос friend_id кто принимает
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
        if Friend.objects.filter(friend_id=friend_id).filter(user_id=request.user.id).exists():
            friend_user = Friend.objects.filter(friend_id=friend_id).filter(user_id=request.user.id).get()
            friend_user.status = "ACCEPTED"
            friend_user.save()
            user_friend = Friend(friend_id=request.user.id, user_id=friend_id, status="ACCEPTED")
            user_friend.save()
            return Response(data={"message": "Друг добавлен"}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def request_to_add_friend(request: Request, friend_id: int) -> Response:
    try:
        CustomUser.objects.get(id=friend_id)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        if Friend.objects.filter(friend_id=friend_id).filter(user_id=request.user.id).exists():
            return Response(data={"message": "Такой запрос в друзья уже есть"}, status=status.HTTP_400_BAD_REQUEST)
        friend_user = Friend(friend_id=friend_id, user_id=request.user.id)
        Friend.objects.bulk_create([friend_user])
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
