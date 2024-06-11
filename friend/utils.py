from friend.models import Friend


def check_duplicate_friends(user_id: int, friend_id: int) -> bool:
    return Friend.objects.filter(user_id=user_id, friend=friend_id).exists()
