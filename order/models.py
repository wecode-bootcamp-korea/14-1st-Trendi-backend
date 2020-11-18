from django.db import models

from core      import models as core_models

class Order(core_models.TimeStampedModel):
    number      = models.CharField(max_length=100)
    status      = models.IntegerField()
    destination = models.ForeignKey('user.Destination',on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'orders'
    
    def __str__(self):
        return self.number

class OrderList(core_models.TimeStampedModel):
    delivery_fee = models.IntegerField(null=True, default=0)
    quantity     = models.IntegerField(null=True)
    user         = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    order        = models.ForeignKey('order.Order', on_delete=models.SET_NULL, null=True)
    product      = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'order_lists'
