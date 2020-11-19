from django.db import models

from core      import models as core_models

class Product(core_models.TimeStampedModel):
    title           = models.CharField(max_length=300)
    thumb_image_url = models.URLField(max_length=1000)
    price           = models.IntegerField()
    description     = models.TextField(null=True)
    seller          = models.ForeignKey('user.Seller', on_delete=models.CASCADE)
    delivery        = models.ForeignKey('product.Delivery', on_delete=models.CASCADE)
    sale            = models.ForeignKey('product.Sale', on_delete=models.CASCADE, null=True)
    category        = models.ForeignKey('product.Category', on_delete=models.CASCADE)
    sub_category    = models.ForeignKey('product.SubCategory', on_delete=models.CASCADE)
    size            = models.ManyToManyField('product.Size', through = "ProductSize", related_name='sizes')
    color           = models.ManyToManyField('product.Color', through = "ProductColor", related_name='colors')

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.title

class ProductDetailImage(core_models.TimeStampedModel):
    detail_image_url  = models.URLField(max_length=1000, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_detail_urls'

class Sale(models.Model):
    sale_ratio = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = 'sale_ratios'
    
    def __str__(self):
        return str(self.sale_ratio)

class Delivery(models.Model):
    delivery_type = models.IntegerField()

    class Meta:
        db_table = 'deliveries'

    def __str__(self):
        return str(self.delivery_type)

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name     = models.CharField(max_length=50)
    category = models.ForeignKey('product.Category', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'sizes'

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('product.Size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_sizes'

class Color(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'colors'

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    color   = models.ForeignKey('product.Color', on_delete=models.CASCADE)

    class Meta:
        db_table = 'products_colors'
