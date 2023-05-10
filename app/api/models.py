from django.db import models
from django.contrib.auth.models import User


class Invite(models.Model):
    from_user = models.ForeignKey(User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="to_user", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('from_user', 'to_user',)


class Friends(models.Model):
    user1 = models.ForeignKey(User, related_name="user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="user2", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user1', 'user2',)