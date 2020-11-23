#import csv
#import os
#import django

# ai reset
# ALTER TABLE table_name AUTO_INCREMENT = 1
# ALTER TABLE categories AUTO_INCREMENT = 1
# ALTER TABLE sub_categories AUTO_INCREMENT = 1
# SET FOREIGN_KEY_CHECKS = 0;
# TRUNCATE table $table_name;
# SET FOREIGN_KEY_CHECKS = 1;
#
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trendi.settings")
#django.setup()
#
#from user.models import *
#from product.models import *
#from order.models import *
#from review.models import *
#
# CSV_PATH_1 = "csv/1_categories.csv"

# with open(CSV_PATH_1, newline='', encoding='utf-8-sig') as csv_file:
#     data_reader = csv.reader(csv_file)
#     next(data_reader, None)

#     for row in data_reader:
#         name = row[1]

#         Category.objects.create(
#             name=name
#         )

#     print("categories 데이터가 정상적으로 추가되었습니다.")
# CSV_PATH_2 = "csv/2_sub_categories.csv"

# with open(CSV_PATH_2, newline='', encoding='utf-8-sig') as csv_file:
#     data_reader = csv.reader(csv_file)
#     next(data_reader, None)

#     for row in data_reader:
#         name = row[1]
#         cate_id = row[2]
#         category = Category.objects.get(id=cate_id)

#         SubCategory.objects.create(
#             name=name,
#             category=category
#         )

#     print("sub_categories 데이터가 정상적으로 추가되었습니다.")


# CSV_PATH_3 = "csv/3_colors.csv"

# with open(CSV_PATH_3, newline='', encoding='utf-8-sig') as csv_file:
#     data_reader = csv.reader(csv_file)
#     next(data_reader, None)

#     for row in data_reader:
#         name = row[1]

#         Color.objects.create(
#             name=name,
#         )

#     print("colors 데이터가 정상적으로 추가되었습니다.")


# CSV_PATH_4 = "csv/4_size.csv"

# with open(CSV_PATH_4, newline='', encoding='utf-8-sig') as csv_file:
#     data_reader = csv.reader(csv_file)
#     next(data_reader, None)

#     for row in data_reader:
#         name = row[1]

#         Size.objects.create(
#             name=name,
#         )

#     print("sizes 데이터가 정상적으로 추가되었습니다.")


# CSV_PATH_5 = "csv/5_sale_ratios.csv"

# with open(CSV_PATH_5, newline='', encoding='utf-8-sig') as csv_file:
#     data_reader = csv.reader(csv_file)
#     next(data_reader, None)

#     for row in data_reader:
#         sale_ratio = row[1]

#         Sale.objects.create(
#             sale_ratio=sale_ratio
#         )

#     print("sale_ratios 데이터가 정상적으로 추가되었습니다.")


# print("=================================================================================")
# print("Seller Data")
# CSV_PATH6 = "csv/6_seller.csv"

# with open(CSV_PATH6, newline='', encoding='utf-8-sig') as csv_file:
#     data_reader = csv.reader(csv_file)
#     next(data_reader, None)

#     for row in data_reader:
#         name = row[1]
#         description = row[2]
#         hash_tag = row[3]
#         image_url = row[4]

#         Seller.objects.create(
#             name=name,
#             description=description,
#             hash_tag=hash_tag,
#             image_url=image_url
#         )

#     print("sellers 데이터가 정상적으로 추가되었습니다.")
# print("=================================================================================")
# print("Delivery")
# Delivery.objects.create(
#     delivery_type = 0
# )
# Delivery.objects.create(
#     delivery_type = 1
# )
# print("Deliveries 데이터가 정상적으로 추가되었습니다.")
# print("=================================================================================")
# print("Products Data")
# CSV_PATH7 = "csv/7_products.csv"

# with open(CSV_PATH7, newline='', encoding='utf-8-sig') as csv_file:
#     data_reader = csv.reader(csv_file)
#     next(data_reader, None)

#     for row in data_reader:
#         title           = row[0]
#         thumb_image_url = row[1]
#         price           = row[2]
#         description     = row[3]
#         category_id     = row[4]
#         delivery_id     = row[5]
#         sub_category_id = row[6]
#         sale_id         = row[7]
#         seller_id       = row[8]

#         category = Category.objects.get(id=category_id)
#         delivery = Delivery.objects.get(id=delivery_id)
#         sub_category = SubCategory.objects.get(id=sub_category_id)
#         sale = Sale.objects.get(id=sale_id)
#         seller = Seller.objects.get(id=seller_id)

#         product = Product(
#             title = title,
#             thumb_image_url = thumb_image_url,
#             price = price,
#             description = description,
#             category=category,
#             delivery=delivery,
#             sub_category=sub_category,
#             sale=sale,
#             seller=seller,
#         )
#         product.save()
# print("Product 데이터가 정상적으로 추가되었습니다.")
# print("=================================================================================")
# print("8_product_detail_urls Data")
#CSV_PATH8 = "csv/8_product_detail_urls.csv"
#
#with open(CSV_PATH8, newline='', encoding='utf-8-sig') as csv_file:
#    data_reader = csv.reader(csv_file)
#    next(data_reader, None)
#
#    for row in data_reader:
#        detail_image_url = row[1]
#        product_id = row[2]
#
#        product = Product.objects.get(id=product_id)
#
#        product_detail_image = ProductDetailImage(
#            detail_image_url = detail_image_url,
#            product = product
#        )
#
#        product_detail_image.save()
#print("product_detail_urls 데이터가 정상적으로 추가되었습니다.")
#OrderStatus.objects.create(status=1)
#OrderStatus.objects.create(status=2)
#OrderStatus.objects.create(status=3)
#OrderStatus.objects.create(status=4)
#print("OrderStatus 데이터가 정상적으로 추가되었습니다.")
#