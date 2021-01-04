import traceback

import pymysql

from utils.custom_exceptions import DatabaseError


class ProductListDao:
    """ Persistence Layer

        Attributes: None

        Author: 김민구, 김기용

        History:
            2020-12-30(김민구): 초기 생성
            2020-12-31(김민구): 에러 문구 변경
    """

    def get_search_products_dao(self, connection, data):
        """ 상품 검색 및 정렬

        """

        sql = """
        SELECT
            product_image.image_url AS image
            , product.name
            , product.seller_id AS seller_id
            , seller.name AS seller_name
            , product.id AS product_id
            , product.origin_price
            , product.discounted_price
            , product_sales_volume.sales_count
        FROM
            products AS product
        INNER JOIN product_images AS product_image
            ON product_id = product_image.product_id
            AND product_image.order_index = 1
        INNER JOIN sellers AS seller
            ON seller.account_id = product.seller_id
        INNER JOIN product_sales_volumes AS product_sales_volume
            ON product_sales_volume.product_id = product.id
        WHERE
            product.name LIKE %(search)s
        ORDER BY
            (CASE WHEN %(sort_type)s=2 THEN sales_count END) DESC
            , (CASE WHEN %(sort_type)s=3 THEN product.id END) DESC
        LIMIT %(limit)s;

        """
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            data['search'] = '%%' + data['search'] + '%%' 
            cursor.execute(sql, data)
            result = cursor.fetchall()
            return result

    def get_product_list(self, connection, event_id):

        """ 상품 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                event_id   : 서비스에서 넘겨 받은 int

            Author: 김민구

            Returns: 30개의 상품정보
                [
                    {
                        'image': 'url',
                        'seller_id': 1,
                        'seller_name': '둘리',
                        'product_id': 1,
                        'product_name': '성보의 하루',
                        'origin_price': 10000.0,
                        'discount_rate': 0.1,
                        'discounted_price': 9000.0,
                        'sales_count': 30
                    },
                ]

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경 / 이벤트에 대한 상품을 반환하는 작업으로 수정
        """

        sql = """
            SELECT 
                product_image.image_url
                , product.seller_id AS seller_id
                , seller.`name` AS seller_name
                , product.id AS product_id
                , product.`name` AS product_name
                , product.origin_price
                , product.discount_rate
                , product.discounted_price 
                , product_sales_volume.sales_count
            FROM
            events_products AS event_product
            INNER JOIN products AS product
                ON event_product.product_id = product.id
            INNER JOIN product_images AS product_image
                ON product_image.product_id = product.id
            INNER JOIN sellers AS seller
                ON seller.account_id = product.seller_id
            INNER JOIN product_sales_volumes AS product_sales_volume
                ON product_sales_volume.product_id = product.id
            WHERE
                event_id = %s
                AND product.is_deleted = 0
                AND product.is_display = 1
            ORDER BY
                product.id DESC
            LIMIT 30;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, event_id)
                result = cursor.fetchall()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

    def get_event(self, connection, offset):
        """ 상품 리스트 조회

            Args:
                connection : 데이터베이스 연결 객체
                offset     : 서비스에서 넘겨 받은 int

            Author: 김민구

            Returns:
                {
                    event_id: 1,
                    event_banner_image: 'url'
                }

            Raises:
                500, {'message': 'database_error', 'error_message': '서버에 알 수 없는 에러가 발생했습니다.'} : 데이터베이스 에러

            History:
                2020-12-30(김민구): 초기 생성
                2020-12-31(김민구): 에러 문구 변경 / 1개의 이벤트 배너 반환하는 작업으로 수정
        """

        sql = """
            SELECT 
                id AS event_id
                , banner_image AS event_banner_image
            FROM 
                events
            WHERE 
                end_date > now()
                AND is_display = 1
                AND is_deleted = 0
            ORDER BY 
                id ASC
            LIMIT %s, 1
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, offset)
                result = cursor.fetchone()
                return result

        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')


    def get_product_detail_dao(self, connection, data):

        sql = """
            SELECT
	        product.id
	        , product.name
                , product.seller_id AS seller_id
                , seller.name AS seller_name
	        , product.origin_price
	        , product.discount_rate
                , product.discounted_price
                , product.detail_infomation
                , product_sales_volume.sales_count
                , bookmark.bookmark_count
            FROM
	        products AS product
	    INNER JOIN sellers AS seller
		ON product.seller_id = seller.account_id
	    INNER JOIN product_sales_volumes AS product_sales_volume
		ON product_sales_volume.product_id = product.id
            INNER JOIN bookmark_volumes AS bookmark
                ON bookmark.product_id = product.id
            WHERE 
	        product.id = %(product_id)s;

        """
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()
                return result
        except Exception:
            traceback.print_exc()
            raise DatabaseError('서버에 알 수 없는 에러가 발생했습니다.')

