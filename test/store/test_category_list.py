from unittest import TestCase

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import config
from app import create_app
from utils.connection import get_connection


class TestCagetoryList(TestCase):
    """ Test

        Target: store/category_list_view

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
        self.connection.commit()
        self.connection.close()

    def tearDown(self):
        self.connection = get_connection(self.app.config['DB'])
        with self.connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate menus')
            cursor.execute('truncate main_categories')
            cursor.execute('truncate sub_categories')
            cursor.execute('set foreign_key_checks=1')
        self.connection.close()

    def test_get_category_list(self):
        response = self.client.get('/categories')
        result = [
            {
                'id': 5,
                'main_categories': [
                    {
                        'id': 12,
                        'menu_id': 5,
                        'name': '아우터',
                        'sub_categories': [
                            {
                                'id': 62,
                                'main_category_id': 12,
                                'name': '코트'
                            }
                        ]
                    }
                ],
                'name': '브랜드'
            }
        ]

        assert response.status_code == 200
        assert json.loads(response.data)['result'] == result