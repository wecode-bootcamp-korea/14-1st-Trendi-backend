from django.db import models

from core      import models as core_models

class Order(core_models.TimeStampedModel):
    number       = models.CharField(max_length=100)
    delivery_fee = models.IntegerField(null=True, default=0)
    user         = models.ForeignKey("user.User", on_delete=models.CASCADE)
    orderstatus  = models.ForeignKey("order.OrderStatus", on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    status = models.IntegerField()

    class Meta:
        db_table = 'status'
    
    def __str__(self):
        return self.status

class OrderStatus(models.Model):
    status = models.IntegerField()

    class Meta:
        db_table = 'status'
    
    def __str__(self):
        return self.status

class OrderList(core_models.TimeStampedModel):
    quantity     = models.IntegerField(null=True)
    order        = models.ForeignKey('order.Order', on_delete=models.SET_NULL, null=True)
    product      = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    size         = models.ForeignKey("product.Size",on_delete=models.CASCADE, null=True)
    color        = models.ForeignKey("product.Color",on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'order_lists'

class Destination(core_models.TimeStampedModel):
    recipient    = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=45)
    address      = models.CharField(max_length=500)
    memo         = models.TextField(null=True)
    default_flag = models.BooleanField(default=True)
    order        = models.ForeignKey("order.Order", on_delete=models.CASCADE)

    class Meta:
        db_table = 'destinations'

    def __str__(self):
        return self.recipient