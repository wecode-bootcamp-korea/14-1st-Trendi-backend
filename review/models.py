from django.db import models

from core      import models as core_models

class Review(core_models.TimeStampedModel):
    content          = models.TextField()
    image_url        = models.URLField(max_length=1000, null=True, blank=True)
    star             = models.IntegerField(max_length=1, blank=True)
    user_information = models.CharField(max_length=200, null=True)
    user             = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product          = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return self.content