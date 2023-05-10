from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Invite, Friends


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username",)


class InvitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ("from_user", )


class InvitesSentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ("to_user",)


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = ("user1", "user2")
