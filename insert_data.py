import csv
import os
import django
import random
from django.db.models import Max
from datetime import date, datetime, timedelta
from django.utils import timezone
import pytz

# unset constraint =======================================================
# SET FOREIGN_KEY_CHECKS = 0;
# SET FOREIGN_KEY_CHECKS = 1;

# reset AI =======================================================
# ALTER TABLE categories AUTO_INCREMENT = 1
# ALTER TABLE sub_categories AUTO_INCREMENT = 1
# ALTER TABLE orders AUTO_INCREMENT = 1;
# ALTER TABLE order_lists AUTO_INCREMENT = 1;
# ALTER TABLE deliveries AUTO_INCREMENT = 0;

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trendi.settings")
django.setup()

from user.models import *
from product.models import *
from order.models import *
from review.models import *


def insert_category():
    CSV_PATH_1 = "csv/1_categories.csv"
    with open(CSV_PATH_1, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            name = row[1]
            Category.objects.create(
                name=name
            )
    print("=================================================================================")
    print("categories 데이터가 정상적으로 추가되었습니다.")


def insert_sub_category():
    CSV_PATH_2 = "csv/2_sub_categories.csv"
    with open(CSV_PATH_2, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            name = row[1]
            cate_id = row[2]
            category = Category.objects.get(id=cate_id)
            SubCategory.objects.create(
                name=name,
                category=category
            )
    print("=================================================================================")
    print("sub_categories 데이터가 정상적으로 추가되었습니다.")


def insert_colors():
    CSV_PATH_3 = "csv/3_colors.csv"
    with open(CSV_PATH_3, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            name = row[1]
            Color.objects.create(
                name=name,
            )
    print("=================================================================================")
    print("colors 데이터가 정상적으로 추가되었습니다.")


def insert_size():
    CSV_PATH_4 = "csv/4_size.csv"
    with open(CSV_PATH_4, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            name = row[1]
            Size.objects.create(
                name=name,
            )
    print("=================================================================================")
    print("sizes 데이터가 정상적으로 추가되었습니다.")


def insert_sale_ratios():
    CSV_PATH_5 = "csv/5_sale_ratios.csv"
    with open(CSV_PATH_5, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            sale_ratio = row[1]
            Sale.objects.create(
                sale_ratio=sale_ratio
            )
    print("=================================================================================")
    print("sale_ratios 데이터가 정상적으로 추가되었습니다.")


def insert_seller():
    CSV_PATH6 = "csv/6_seller.csv"
    with open(CSV_PATH6, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            name = row[1]
            description = row[2]
            hash_tag = row[3]
            image_url = row[4]
            Seller.objects.create(
                name=name,
                description=description,
                hash_tag=hash_tag,
                image_url=image_url
            )
    print("=================================================================================")
    print("sellers 데이터가 정상적으로 추가되었습니다.")


def insert_delivery():
    Delivery.objects.create(
        delivery_type = 0
    )
    Delivery.objects.create(
        delivery_type = 1
    )
    print("=================================================================================")
    print("Deliveries 데이터가 정상적으로 추가되었습니다.")


def insert_products():
    CSV_PATH7 = "csv/7_products.csv"

    with open(CSV_PATH7, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        
        for row in data_reader:
            title           = row[0]
            thumb_image_url = row[1]
            price           = row[2]
            description     = row[3]
            category_id     = row[4]
            delivery_id     = row[5]
            sub_category_id = row[6]
            sale_id         = row[7]
            seller_id       = row[8]
            
            category = Category.objects.get(id=category_id)
            delivery = Delivery.objects.get(id=delivery_id)
            sub_category = SubCategory.objects.get(id=sub_category_id)
            sale = Sale.objects.get(id=sale_id)
            seller = Seller.objects.get(id=seller_id)
            
            product = Product(
                title = title,
                thumb_image_url = thumb_image_url,
                price = price,
                description = description,
                category=category,
                delivery=delivery,
                sub_category=sub_category,
                sale=sale,
                seller=seller,
            )
            product.save()
    print("=================================================================================")
    print("Product 데이터가 정상적으로 추가되었습니다.")


def product_details():
    CSV_PATH8 = "csv/8_product_detail_urls.csv"
    
    with open(CSV_PATH8, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        
        for row in data_reader:
            detail_image_url = row[1]
            product_id = row[2]

            product = Product.objects.get(id=product_id)

            product_detail_image = ProductDetailImage(
                detail_image_url = detail_image_url,
                product = product
            )

            product_detail_image.save()
    print("=================================================================================")
    print("product_detail_urls 데이터가 정상적으로 추가되었습니다.")


def insert_orderstatus():
    OrderStatus.objects.create(status=1)
    OrderStatus.objects.create(status=2)
    OrderStatus.objects.create(status=3)
    OrderStatus.objects.create(status=4)
    OrderStatus.objects.create(status=5)
    print("=================================================================================")
    print("OrderStatus 데이터가 정상적으로 추가되었습니다.")


def insert_user():
    CSV_PATH9 = "csv/9_user.csv"
    with open(CSV_PATH9, newline='', encoding='utf-8-sig') as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            nick_name = row[0]
            password = row[1]
            email = row[2]
            user_name = row[3]
            phone_number = row[4]
            user = User(
                nick_name = nick_name,
                password = password,
                email = email,
                user_name = user_name,
                phone_number = phone_number
            )
            user.save()
    print("=================================================================================")
    print("User 데이터가 정상적으로 추가되었습니다.")


def insert_reviews():
    content = [
        "만족합니다. 별 다섯개 드립니다. 짱짱!!",
        "가격 대비 입기 좋아요. 그런데 한 번 빨면 옷감이 조금 상해요..ㅠㅠ",
        "넘 마음에들고 이뻐요..! 슬림이라서 더 얇아보이는 효과가 있기도하고 ??",
        "재질도 부드럽고 핏도 예쁘고 데일리로 입기 좋아요!ㅎㅎ",
        "만족하지만 배송이 조금 느렸습니다...",
        "완전히 핏되진 않은데 이가격에 두개면 개이득입니다.. ! ^^",
    ]

    for row in range(1, 8000):
        product = Product.objects.get(id=random.randint(1, 100))
        review = Review(
            content = content[random.randint(0, len(content)-1)],
            star = random.randint(1, 5),
            user = User.objects.get(id=random.randint(1, 99)),
            product = product
        )
        review.save()
    print("=================================================================================")
    print("reviews 데이터가 정상적으로 추가되었습니다.")


order_status = {
    1 : '장바구니',
    2 : '주문/결제',
    3 : '주문완료',
    4 : '배송중',
    5 : '배송완료'
}

def insert_basic_order():
    # 주문 기본 데이터
    # 유저 1에서 10이 구매하는 새로운 1개의 오더가 만들어짐
    ordered = Order.objects.create(
        order_number=str(1000),
        delivery_fee = 0,
        user=User.objects.get(id=random.randint(1, 10)),
        orderstatus=OrderStatus.objects.get(id=random.randint(2, 5)),
    )
    
    order_list = OrderList(
        quantity=random.randint(1, 2),
        order=ordered,
        product=Product.objects.get(id=random.randint(1, 10)),
        size = Size.objects.get(id=random.randint(1, 6)),
        color = Color.objects.get(id=random.randint(1, 17))
    )
    order_list.save()


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def insert_order_lists():
    d1 = datetime.strptime('11/24/2020 10:30 AM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('11/26/2020 4:50 AM', '%m/%d/%Y %I:%M %p')

    for i in range(1, 1000):
        # order_id +1 시키기
        new_order_id = Order.objects.all().aggregate(Max('id'))['id__max'] + 1

        # order_number +1 시키기 (현재 str 값)
        order_number = Order.objects.all().aggregate(Max('order_number'))['order_number__max']
        new_order_number = str(int(order_number) + 1)

        # 2020/10/20 ~ 2020/11/21 까지의 랜덤 날짜
        ordered_date = random_date(d1, d2)
        
        ordered = Order.objects.create(
            order_number = new_order_number,
            user = User.objects.get(id=random.randint(1, 10)),
            orderstatus = OrderStatus.objects.get(id=random.randint(1, 5)),
        )
        
        product_ids = []
        for i in range(0, 3):
            product_ids.append((random.randint(1, 253)))
        
        product_ids_set = list(set(product_ids))
        
        for i in range(len(product_ids_set)):
            OrderList.objects.create(
                quantity = random.randint(1, 3),
                order = ordered,
                product = Product.objects.get(id=product_ids_set[i]),
            )
        
        Order.objects.filter(order_number=new_order_number).update(updated_at=ordered_date)
        order = Order.objects.get(order_number=new_order_number)
        OrderList.objects.filter(order=order).update(updated_at=ordered_date)
    print("=================================================================================")
    print("order 데이터 10000개가 정상적으로 추가되었습니다.")
    print("order_list 10000개가 데이터가 정상적으로 추가되었습니다.")
    print("만들어진 데이터는 order_status 1~5 까지의 데이터 입니다.")
    print("=================================================================================")


# 상품번호 1~200 까지 각각 색상 넣기
# 색상은 최소 1개는 있어야 한다.
# 색상은 최대 3개까지만 넣는다.
# 25프로의 확률로 색상 데이터가 들어가지 않는다.
def insert_products_colors():
    for product_id in range(1, 253):
        random_ids = set()
        for i in range(0, 3):
            random_ids.add(random.randint(1, 17))
        
        product = Product.objects.get(id=product_id)
        for id in set(random_ids):
            color = Color.objects.get(id=id)
            ProductColor.objects.create(
                product=product,
                color=color
            )
            # if random.randint(0, 3):
            #     color = Color.objects.get(id=id)
            #     ProductColor.objects.create(
            #         product=product,
            #         color=color
            #     )


# 상품번호 1~200 까지 각각 색상 넣기
# 사이즈는 최소 1개는 있어야 한다.
# 사이즈는 최대 2개까지만 넣는다.
# 25프로의 확률로 사이즈 데이터가 들어가지 않는다.
def insert_products_sizes():
    for product_id in range(1, 253):
        random_ids = set()
        for i in range(0, 2):
            random_ids.add(random.randint(1, 6))
        
        product = Product.objects.get(id=product_id)
        for id in random_ids:
            size = Size.objects.get(id=id)
            ProductSize.objects.create(
                product=product,
                size=size
            )

insert_category()
insert_sub_category()
insert_colors()
insert_size()
insert_sale_ratios()
insert_seller()
insert_delivery()
insert_products()
insert_orderstatus()
insert_user()
insert_reviews()
insert_basic_order()
insert_order_lists()
insert_products_colors()
insert_products_sizes()

# 연습
# before_30days = datetime.today() - timedelta(30)
# start_date = datetime.today() - timedelta.days(30)
# print(start_date)

# def before_month(start, end):
#     delta = end - start
#     int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
#     random_second = random.randrange(int_delta)
#     return start + timedelta(seconds=random_second)
#
# d1 = datetime.strptime('10/20/2020 10:30 AM', '%m/%d/%Y %I:%M %p')
# d2 = datetime.strptime('11/21/2020 4:50 AM', '%m/%d/%Y %I:%M %p')
#
# ordered_date = random_date(d1, d2)


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

# updated_at 랜덤으로 업데이트
def update_products_date():
    d1 = datetime.strptime('10/20/2020 10:30 AM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('11/24/2020 4:50 AM', '%m/%d/%Y %I:%M %p')

    for i in range(1, 301):
        Product.objects.filter(id=i).update(updated_at=random_date(d1, d2))


# insert random 0 or 1 to products brandi_pick column
# for i in range(1, 301):
#     product = Product.objects.get(id=i)
#     product.brandi_pick = random.randint(0, 1)
#     product.save()

# yesterday = datetime.today() - timedelta(days=1)
#
# products = Product.objects.filter(updated_at__gt=yesterday)
# for p in products:
#     print(p.updated_at)
    # print(p.values('updated_at'))


# yesterday = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
# print(yesterday)
#
# products = OrderList.objects.filter(updated_at__gt=yesterday)








