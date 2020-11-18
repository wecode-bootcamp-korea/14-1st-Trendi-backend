from django.db import models

from core      import models as core_models

class User(core_models.TimeStampedModel):
    nick_name    = models.CharField(max_length=20)
    password     = models.CharField(max_length=45)
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

class Destination(core_models.TimeStampedModel):
    recipient    = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=45)
    address      = models.CharField(max_length=500)
    memo         = models.TextField(null=True)
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE)
    default_flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'destinations'

    def __str__(self):
        return self.recipient