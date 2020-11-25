from django.db import models

class ProductFavor(models.Model):
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE,)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE,)

    class Meta:
        db_table = 'product_favors'

class SellerFavor(models.Model):
    user   = models.ForeignKey('user.User', on_delete=models.CASCADE)
    seller = models.ForeignKey('user.Seller', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'seller_favors'
