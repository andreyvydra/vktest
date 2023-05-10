from django.urls import path

from .views import CreateUserAPI, InviteAPI, AcceptInviteAPI, DeclineInviteAPI, ShowInvitesAPI, ShowSentInvitesAPI, \
    ShowFriendsAPI, UserStatusAPI, DeleteFriendAPI

urlpatterns = [
    path('create_user', CreateUserAPI.as_view()),
    path('user/<int:from_user>/invite/<int:to_user>', InviteAPI.as_view()),
    path('user/<int:to_user>/accept/<int:from_user>', AcceptInviteAPI.as_view()),
    path('user/<int:to_user>/decline/<int:from_user>', DeclineInviteAPI.as_view()),
    path('user/<int:user>/invites', ShowInvitesAPI.as_view()),
    path('user/<int:user>/sent_invites', ShowSentInvitesAPI.as_view()),
    path('user/<int:user>/friends', ShowFriendsAPI.as_view()),
    path('user/<int:from_user>/status/<int:to_user>', UserStatusAPI.as_view()),
    path('user/<int:from_user>/delete_friend/<int:to_user>', DeleteFriendAPI.as_view()),
]