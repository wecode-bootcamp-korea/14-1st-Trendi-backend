from django.db import models

from core      import models as core_models

class User(core_models.TimeStampedModel):
    nick_name    = models.CharField(max_length=20)
    password     = models.CharField(max_length=100)
    email        = models.EmailField(max_length=100)
    user_name    = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.nick_name

class Seller(core_models.TimeStampedModel):
    name        = models.CharField(max_length=100)
    description = models.TextField(null=True)
    hash_tag    = models.TextField(null=True)
    image_url   = models.URLField(max_length=1000)

    class Meta:
        db_table = 'sellers'

    def __str__(self):
        return self.name

