from django.db import models


class Dummy(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)

