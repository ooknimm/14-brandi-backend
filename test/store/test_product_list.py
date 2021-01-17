from unittest import TestCase

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import config
from app import create_app
from utils.connection import get_connection


class TestProductList(TestCase):
    """ Test

        Target: store/product_list_view

        Author: 김민구

        History:
            2021-01-16(김민구): 초기 생성
    """

    def setUp(self):
        self.app = create_app(config.test_config)
        self.connection = get_connection(self.app.config['DB'])
        self.client = self.app.test_client()

        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO event_kinds (`id`, `name`) VALUES (1, '상품');")
            cursor.execute("INSERT INTO event_types (`id`, `name`) VALUES (1, '상품(이미지)')")
            cursor.execute("INSERT INTO event_types_kinds (`id`, `event_type_id`, `event_kind_id`) VALUES (1, 1, 1)")
            cursor.execute("INSERT INTO menus (`id`, `name`) VALUES (5, '브랜드')")
            cursor.execute("INSERT INTO main_categories (`id`, `name`, `menu_id`) VALUES (12, '아우터', 5)")
            cursor.execute("INSERT INTO sub_categories (`id`, `name`, `main_category_id`) VALUES (62, '코트', 12)")
            cursor.execute("INSERT INTO product_origin_types (`id`, `name`) VALUES (1, '기타')")
            cursor.execute("INSERT INTO permission_types (`id`, `name`) VALUES (2, '셀러')")
            cursor.execute("INSERT INTO seller_status_types (`id`, `name`) VALUES (2, '입점')")
            cursor.execute("INSERT INTO seller_attribute_types (`id`, `name`, `menu_id`) VALUES (4, '디자이너브랜드', 5)")
            cursor.execute("""
                INSERT INTO accounts (
                    id
                    , username
                    , `password`
                    , permission_type_id
                ) VALUES (
                    1
                    , 'seller'
                    , '1234'
                    , 2
            )""")
            cursor.execute("""
                INSERT INTO sellers (
                    account_id
                    , seller_status_type_id
                    , seller_attribute_type_id
                    , `name`
                    , english_name
                    , contact_phone
                    , service_center_number
                    , profile_image_url
                    , background_image_url
                    , seller_title
                    , seller_discription
                    , contact_name
                    , contact_email
                    , address1
                    , address2
                    , post_number
                    , operation_start_time
                    , operation_end_time
                    , exchange_information
                    , shipping_information
                ) VALUES (
                    1
                    , 2
                    , 4
                    , '나는셀러'
                    , 'i am seller_'
                    , '01012341234'
                    , '023331111'
                    , 'profile_url'
                    , 'background_url'
                    , '셀러 한 줄 설명_'
                    , 'seller_description'
                    , 'contact_name'
                    , 'contact@test.com'
                    , '서울시 강남구 테헤란로 48-2'
                    , '위워크 10층'
                    , '123-123'
                    , '09:00'
                    , '18:00'
                    , '교환 안됨'
                    , '배송 곧 감'
            )""")
            cursor.execute("""
                INSERT INTO products (
                    id
                    , `name`
                    , `product_code`
                    , `is_display`
                    , `is_sale`
                    , `main_category_id`
                    , `sub_category_id`
                    , `is_product_notice`
                    , `manufacturer`
                    , `manufacturing_date`
                    , `product_origin_type_id`
                    , `description`
                    , `detail_information`
                    , `origin_price`
                    , `discount_rate`
                    , `discounted_price`
                    , `discount_start_date`
                    , `discount_end_date`
                    , `minimum_quantity`
                    , `maximum_quantity`
                    , `seller_id`
                    , `account_id`
                ) VALUES (
                    1
                    , '성보의하루'
                    , 'P1111'
                    , 1
                    , 1
                    , 12
                    , 62
                    , 0
                    , '패션의 완성 위코드(제조)'
                    , '2020-01-01'
                    , 1
                    , '상품 설명'
                    , 'html======================================================'
                    , 10000
                    , 0.1
                    , 9000
                    , '2020-11-01 09:00'
                    , '2021-12-25 23:59'
                    , 1
                    , 20
                    , 1
                    , 1
            )""")
            cursor.execute("""
                INSERT INTO product_sales_volumes (
                    product_id
                    , sales_count
                ) VALUES (
                    1
                    , 1000
            )""")
            cursor.execute("""
                INSERT INTO product_images (
                    product_id
                    , image_url
                    , order_index
                ) VALUES (
                    1
                    , 'product_url'
                    , 1
            )""")
            cursor.execute("""
                INSERT INTO `events` (
                    id
                    , `name`
                    , `start_date`
                    , `end_date`
                    , `banner_image`
                    , `detail_image`
                    , `event_type_id`
                    , `event_kind_id`
                    , `is_display`
                ) VALUES (
                    1
                    , '성보의 내일'
                    , '2020-10-19 00:00:00'
                    , '2021-03-01 00:00:00'
                    , 'banner_url'
                    , 'detail_url'
                    , 1
                    , 1
                    , 1
            )""")
            cursor.execute("INSERT INTO events_products (event_id, product_id) VALUES (1, 1)")
        self.connection.commit()
        self.connection.close()

    def tearDown(self):
        self.connection = get_connection(self.app.config['DB'])
        with self.connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate accounts')
            cursor.execute('truncate sellers')
            cursor.execute('truncate permission_types')
            cursor.execute('truncate events')
            cursor.execute('truncate event_kinds')
            cursor.execute('truncate event_types')
            cursor.execute('truncate event_types_kinds')
            cursor.execute('truncate menus')
            cursor.execute('truncate main_categories')
            cursor.execute('truncate sub_categories')
            cursor.execute('truncate product_origin_types')
            cursor.execute('truncate seller_status_types')
            cursor.execute('truncate seller_attribute_types')
            cursor.execute('truncate products')
            cursor.execute('truncate product_sales_volumes')
            cursor.execute('truncate product_images')
            cursor.execute('truncate events_products')
            cursor.execute('set foreign_key_checks=1')
        self.connection.close()

    def test_get_product_list(self):
        response = self.client.get('/products')
        result = {
            'event': {
                'event_banner_image': 'banner_url',
                'event_id': 1
            },
            'product_list': [
                {
                    'discount_rate': 0.1,
                    'discounted_price': 9000,
                    'image_url': 'product_url',
                    'origin_price': 10000,
                    'product_id': 1,
                    'product_name': '성보의하루',
                    'sales_count': 1000,
                    'seller_id': 1,
                    'seller_name': '나는셀러'
                }
            ]
        }

        assert response.status_code == 200
        assert json.loads(response.data)['result'] == result
