from django.db import models

class PrivateGroupQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(memberships__user=user).distinct()
