import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trendi.settings")
django.setup()

from user.models import User, Seller
from product.models import (
    Product, ProductDetailImage, Color, Size, Sale, Delivery,
    Category, SubCategory
)
from order.models import Order, OrderStatus, OrderList, Destination
from review.models import Review

print("=================전체 데이터 삭제 시작=================")
# User.objects.all().delete()
# Seller.objects.all().delete()
# Color.objects.all().delete()
# Size.objects.all().delete()
# Sale.objects.all().delete()
# Delivery.objects.all().delete()
# OrderStatus.objects.all().delete()
# Order.objects.all().delete()
# OrderList.objects.all().delete()
# Destination.objects.all().delete()
# Review.objects.all().delete()
# ProductDetailImage.objects.all().delete()
# SubCategory.objects.all().delete()
# Category.objects.all().delete()
# Product.objects.all().delete()
print("=================전체 데이터 삭제 완료=================")

# select * from users;
# select * from sellers;
# select * from colors;
# select * from sizes;
# select * from sale_ratios;
# select * from deliveries;
# select * from status;
# select * from orders;
# select * from order_lists;
# select * from destinations;
# select * from reviews;
# select * from product_detail_urls;
# select * from sub_categories;
# select * from categories;
# select * from products;
# alter table users auto_increment = 1;
# alter table sellers auto_increment = 1;
# alter table colors auto_increment = 1;
# alter table sizes auto_increment = 1;
# alter table sale_ratios auto_increment = 1;
# alter table deliveries auto_increment = 1;
# alter table status auto_increment = 1;
# alter table orders auto_increment = 1;
# alter table order_lists auto_increment = 1;
# alter table destinations auto_increment = 1;
# alter table reviews auto_increment = 1;
# alter table product_detail_urls auto_increment = 1;
# alter table sub_categories auto_increment = 1;
# alter table categories auto_increment = 1;
# alter table products auto_increment = 1;