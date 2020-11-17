from django.db import models

from core      import models as core_models

STAR_ONE   = '1'
STAR_TWO   = '2'
STAR_THREE = '3'
STAR_FOUR  = '4'
STAR_FIVE  = '5'

STAR_GRADE = (
   (STAR_ONE,  '1'),
   (STAR_TWO,  '2'),
   (STAR_THREE,'3'),
   (STAR_FOUR, '4'),
   (STAR_FIVE, '5'),
)

class Review(core_models.TimeStampedModel):
    content   = models.TextField()
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    star      = models.CharField(choices=STAR_GRADE, max_length=10, blank=True)
    user      = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product   = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return self.content