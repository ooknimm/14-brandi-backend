from unittest import TestCase

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import config
from app import create_app
from utils.connection import get_connection


class TestBookMark(TestCase):
    """ Test

        Target: store/bookmark_view

        Author: 김민구

        History:
            2021-01-16(김민구): 초기 생성
    """

    def setUp(self):
        self.app = create_app(config.test_config)
        self.connection = get_connection(self.app.config['DB'])
        self.client = self.app.test_client()

        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO menus (`id`, `name`) VALUES (5, '브랜드')")
            cursor.execute("INSERT INTO main_categories (`id`, `name`, `menu_id`) VALUES (12, '아우터', 5)")
            cursor.execute("INSERT INTO sub_categories (`id`, `name`, `main_category_id`) VALUES (62, '코트', 12)")
            cursor.execute("INSERT INTO product_origin_types (`id`, `name`) VALUES (1, '기타')")
            cursor.execute("INSERT INTO permission_types (`id`, `name`) VALUES (2, '셀러')")
            cursor.execute("INSERT INTO permission_types (`id`, `name`) VALUES (3, '일반유저')")
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
                    2
                    , '성보의하루2'
                    , 'P2222'
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
        self.connection.commit()
        self.connection.close()

        data = json.dumps({
            'username': 'brandi',
            'email': 'brandi@naver.com',
            'phone': '01099998888',
            'password': '1q2w3e$R'
        })

        response = self.client.post(
            '/users/signup',
            data=data,
            content_type='application/json'
        )

        assert response.status_code == 200

        signin_data = json.dumps({
            'username': 'brandi',
            'password': '1q2w3e$R'
        })
        response = self.client.post(
            '/users/signin',
            data=signin_data,
            content_type='application/json'
        )
        assert response.status_code == 200
        self.token = json.loads(response.data)['token']

    def tearDown(self):
        self.connection = get_connection(self.app.config['DB'])
        with self.connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate accounts')
            cursor.execute('truncate sellers')
            cursor.execute('truncate permission_types')
            cursor.execute('truncate menus')
            cursor.execute('truncate bookmarks')
            cursor.execute('truncate users')
            cursor.execute('truncate main_categories')
            cursor.execute('truncate sub_categories')
            cursor.execute('truncate product_origin_types')
            cursor.execute('truncate seller_status_types')
            cursor.execute('truncate seller_attribute_types')
            cursor.execute('truncate products')
            cursor.execute('truncate product_sales_volumes')
            cursor.execute('truncate product_images')
            cursor.execute('set foreign_key_checks=1')
        self.connection.close()

    def test_create_bookmark(self):
        response = self.client.post(
            '/products/1/bookmarks',
            headers={'Authorization': self.token}
        )

        assert response.status_code == 200

    def test_create_bookmark_fail_already_exist(self):
        response = self.client.post(
            '/products/1/bookmarks',
            headers={'Authorization': self.token}
        )

        assert response.status_code == 200

        response = self.client.post(
            '/products/1/bookmarks',
            headers={'Authorization': self.token}
        )

        assert response.status_code == 400
        assert json.loads(response.data)['error_message'] == '이미 추가된 북마크입니다.'

    def test_create_bookmark_fail_product_does_not_exist(self):
        response = self.client.post(
            '/products/11/bookmarks',
            headers={'Authorization': self.token}
        )

        assert response.status_code == 404
        assert json.loads(response.data)['error_message'] == '해당 상품이 존재하지 않습니다.'

    def test_delete_bookmark(self):
        response = self.client.post(
            '/products/1/bookmarks',
            headers={'Authorization': self.token}
        )

        assert response.status_code == 200

        response = self.client.delete(
            '/products/1/bookmarks',
            headers={'Authorization': self.token}
        )

        assert response.status_code == 200

    def test_delete_bookmark_fail_no_token(self):
        response = self.client.post(
            '/products/1/bookmarks',
            headers={'Authorization': self.token}
        )

        assert response.status_code == 200

        response = self.client.delete(
            '/products/1/bookmarks'
        )

        assert response.status_code == 401
        assert json.loads(response.data)['error_message'] == '로그인이 필요합니다.'

    def test_delete_bookmark_fail_bookmark_does_not_exist(self):
        response = self.client.delete(
            '/products/2/bookmarks',
            headers={'Authorization': self.token}
        )

        assert response.status_code == 404
        assert json.loads(response.data)['error_message'] == '해당 북마크가 존재하지 않습니다.'
