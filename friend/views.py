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
        friend_user = Friend.objects.filter(friend_id=request.user.id).filter(user_id=friend_id).filter(
            status="ACCEPTED").first()
        user_friend = Friend.objects.filter(friend_id=friend_id).filter(user_id=request.user.id).filter(
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
        friends = Friend.objects.filter(user_id=request.user.id).filter(status="ACCEPTED").all()
        for friend_request in friends:
            if friend_request.flag_reverse:
                friend_request.flag_reverse = True
    except Friend.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = FriendSerializer(
            friends,
            many=True
        )
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def get_incoming_requests(request: Request) -> Response:
    try:
        friend_requests = Friend.objects.filter(friend_id=request.user.id, status="WAITING")
        for friend_request in friend_requests:
            if friend_request.flag_reverse:
                friend_request.flag_reverse = False
    except Friend.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = FriendSerializer(
            friend_requests,
            many=True
        )
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['GET'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def get_outcoming_requests(request: Request) -> Response:
    try:
        friend_requests = Friend.objects.filter(user_sender_id=request.user.id, status="WAITING",
                                                user_id=request.user.id).all()
        for friend_request in friend_requests:
            if friend_request.flag_reverse:
                friend_request.flag_reverse = True
    except Friend.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = FriendSerializer(
            friend_requests,
            many=True
        )
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def add_friend(request: Request, friend_id: int) -> Response:
    try:
        CustomUser.objects.get(id=request.user.id)
    except CustomUser.DoesNotExist:
        return Response(data={"message": "Такого друга нет"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        user_friend_request = Friend.objects.filter(user_id=friend_id, friend_id=request.user.id,
                                                    status="WAITING").get()
        user_friend_request.status = "ACCEPTED"
        user_friend_request.flag_reverse = True
        user_friend_request.save()
        friend_user_response = Friend(user_id=request.user.id, friend_id=friend_id, status="ACCEPTED",
                                      user_sender_id=friend_id)
        friend_user_response.save()
        return Response(data={"message": "Друг добавлен"}, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['POST'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def request_to_add_friend(request: Request, friend_id: int) -> Response:
    try:
        CustomUser.objects.get(id=friend_id)
    except CustomUser.DoesNotExist:
        return Response(data={"message": "Такого пользователя нет"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        if Friend.objects.filter(friend_id=friend_id).filter(user_id=request.user.id).exists():
            return Response(data={"message": "Такой запрос в друзья уже есть"}, status=status.HTTP_400_BAD_REQUEST)
        user_friend = Friend(friend_id=friend_id, user_id=request.user.id, user_sender_id=request.user.id)
        Friend.objects.bulk_create([user_friend])
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['DELETE'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def reject_request_outcoming_friend(request: Request, friend_id: int) -> Response:
    if request.method == 'DELETE':
        try:
            request_friend = Friend.objects.filter(friend_id=friend_id, user_id=request.user.id, status="WAITING").get()
        except Friend.DoesNotExist:
            return Response(data={"message": "Такого запроса в друзья не было"}, status=status.HTTP_404_NOT_FOUND)
        request_friend.delete()
        return Response(data={"message": "Запрос в друзья удален"}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['DELETE'])
@permission_classes(permission_classes=[IsAuthenticated, ])
def reject_request_incoming_friend(request: Request, friend_id: int) -> Response:
    if request.method == 'DELETE':
        try:
            request_friend = Friend.objects.filter(friend_id=request.user.id, user_id=friend_id, status="WAITING").get()
        except Friend.DoesNotExist:
            return Response(data={"message": "Такого запроса в друзья не было"}, status=status.HTTP_404_NOT_FOUND)
        request_friend.delete()
        return Response(data={"message": "Запрос в друзья удален"}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
