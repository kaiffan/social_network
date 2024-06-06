from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, ValidationError, Serializer
from dialogue.models import Dialogue


class DialogueSerializer(ModelSerializer[Dialogue]):
    class Meta:
        model = Dialogue
        fields = [
            'title',
            'is_chat',
            'is_pinned'
        ]
