from django.db.utils import IntegrityError

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import Invite, Friends
from .serializers import UserSerializer, InvitesSerializer, InvitesSentSerializer, FriendsSerializer

from django.contrib.auth.models import User
from django.db.models import Q


class CreateUserAPI(APIView):
    def post(self, request, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            user_id = User.objects.filter(username=user.data["username"])[0].id
            return Response(user_id, status=HTTP_200_OK)
        return Response("Некорректный запрос", status=HTTP_400_BAD_REQUEST)


class GeneralAPI(APIView):
    def get_users(self, **kwargs):
        from_user_id = kwargs.get("from_user")
        to_user_id = kwargs.get("to_user")
        from_user = User.objects.filter(id=from_user_id)
        to_user = User.objects.filter(id=to_user_id)
        if len(from_user) != 0 and len(to_user) != 0:
            return from_user[0], to_user[0]
        return None, None

    def get_invitation(self, from_user, to_user):
        invite = Invite.objects.filter(from_user=from_user,
                                       to_user=to_user)
        if len(invite) == 0:
            return None
        return invite[0]

    def get_friend(self, from_user, to_user):
        friends = Friends.objects.filter(user1__in=[from_user, to_user], user2__in=[from_user, to_user])
        if len(friends) == 0:
            return None
        return friends[0]


class InviteAPI(GeneralAPI):
    def post(self, request, **kwargs):
        from_user, to_user = self.get_users(**kwargs)
        if from_user is not None and to_user is not None and from_user != to_user:
            if self.get_friend(from_user, to_user) is None:
                try:
                    prev_invite = self.get_invitation(to_user, from_user)
                    if prev_invite is not None:
                        friend = Friends.objects.create(user1=from_user, user2=to_user)
                        friend.save()
                        prev_invite.delete()
                        return Response("Добавлены в друзья", status=HTTP_200_OK)
                    invite = Invite.objects.create(from_user=from_user,
                                                   to_user=to_user)
                    invite.save()
                    return Response("Заявка успешено отправлена", status=HTTP_200_OK)
                except IntegrityError as e:
                    return Response("Запрос в друзья уже был отправлен", status=HTTP_400_BAD_REQUEST)
        return Response("Некорректный запрос", status=HTTP_400_BAD_REQUEST)


class DeclineInviteAPI(GeneralAPI):
    def post(self, request, **kwargs):
        from_user, to_user = self.get_users(**kwargs)
        if from_user is not None and to_user is not None:
            invite = self.get_invitation(from_user, to_user)
            if invite is None:
                return Response("Заявка не найдена", status=HTTP_400_BAD_REQUEST)
            invite.delete()
            return Response("Заявка отклонена", status=HTTP_200_OK)
        return Response("Некорректный запрос", status=HTTP_400_BAD_REQUEST)


class AcceptInviteAPI(GeneralAPI):
    def post(self, request, **kwargs):
        from_user, to_user = self.get_users(**kwargs)
        if from_user is not None and to_user is not None:
            invite = self.get_invitation(from_user, to_user)
            if invite is None:
                return Response("Заявка не найдена", status=HTTP_400_BAD_REQUEST)
            try:
                friend = Friends.objects.create(user1=from_user, user2=to_user)
                friend.save()
                invite.delete()
                return Response("Заявка принята", status=HTTP_200_OK)
            except IntegrityError as e:
                return Response("Пользователи уже друзья", status=HTTP_400_BAD_REQUEST)
        return Response("Некорректный запрос", status=HTTP_400_BAD_REQUEST)


class ShowInvitesAPI(APIView):
    def get(self, request, **kwargs):
        user_id = kwargs.get("user")
        users = User.objects.filter(id=user_id)
        if len(users) != 0:
            user = users[0]
            invites = Invite.objects.filter(to_user=user)
            invites_serial = InvitesSerializer(invites, many=True)
            return Response(invites_serial.data, status=HTTP_200_OK)
        return Response("Некоректный запрос", status=HTTP_400_BAD_REQUEST)


class ShowSentInvitesAPI(APIView):
    def get(self, request, **kwargs):
        user_id = kwargs.get("user")
        users = User.objects.filter(id=user_id)
        if len(users) != 0:
            user = users[0]
            invites = Invite.objects.filter(from_user=user)
            invites_serial = InvitesSentSerializer(invites, many=True)
            return Response(invites_serial.data, status=HTTP_200_OK)
        return Response("Некоректный запрос", status=HTTP_400_BAD_REQUEST)


class ShowFriendsAPI(APIView):
    def get(self, request, **kwargs):
        user_id = kwargs.get("user")
        users = User.objects.filter(id=user_id)
        if len(users) != 0:
            user = users[0]
            friends = Friends.objects.filter(Q(user1=user) | Q(user2=user))
            friends_serial = FriendsSerializer(friends, many=True)
            return Response(friends_serial.data, status=HTTP_200_OK)
        return Response("Некоректный запрос", status=HTTP_400_BAD_REQUEST)


class UserStatusAPI(GeneralAPI):
    def get(self, request, **kwargs):
        from_user, to_user = self.get_users(**kwargs)
        if from_user is not None and to_user is not None:
            invite = self.get_invitation(to_user, from_user)
            sent_invite = self.get_invitation(from_user, to_user)
            friend = self.get_friend(from_user, to_user)
            if invite is not None:
                return Response("Есть входящая заявка", status=HTTP_200_OK)
            elif sent_invite is not None:
                return Response("Есть отправленная заявка", status=HTTP_200_OK)
            elif friend is not None:
                return Response("Друзья", status=HTTP_200_OK)
            return Response("Нет статуса", status=HTTP_200_OK)
        return Response("Некорректный запрос", status=HTTP_400_BAD_REQUEST)


class DeleteFriendAPI(GeneralAPI):
    def post(self, request, **kwargs):
        from_user, to_user = self.get_users(**kwargs)
        if from_user is not None and to_user is not None:
            friend = self.get_friend(from_user, to_user)
            if friend is not None:
                friend.delete()
                return Response("Больше не друзья", status=HTTP_200_OK)
            return Response("Не являются друзьями", status=HTTP_200_OK)
        return Response("Некорректный запрос", status=HTTP_400_BAD_REQUEST)
