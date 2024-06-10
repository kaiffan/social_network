from rest_framework.serializers import ModelSerializer
from dialogue.models import Dialogue
from rest_framework import serializers


class DialogueSerializer(ModelSerializer[Dialogue]):

    class Meta:
        model = Dialogue
        fields = [
            'title',
            'avatar',
            'is_pinned'
        ]
