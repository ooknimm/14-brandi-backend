from utils.custom_exceptions import OrderFilterNotExist, NoPermissionGetOrderList, DateInputDoesNotExist

class OrderService:
    """ Business Layer
            Attributes:
                get_order_list_dao: OrderDao 클래스

            Author: 김민서

            History:
                2020-20-29(김민서): 초기 생성
                2020-12-30(김민서): 1차 수정
                2020-12-31(김민서): 2차 수정
    """
    def __init__(self, master_order_dao):
        self.master_order_dao = master_order_dao

    def get_orders_service(self, connection, data):
        try:
            if not (data['permission'] == 1 or data['permission'] == 2):
                raise NoPermissionGetOrderList('no_permission_to_get_order_list')

            if (data['start_date'] and not data['end_date']) or (not data['start_date'] and data['end_date']):
                raise DateInputDoesNotExist('must_be_other_date_input')

            filters = data['start_date'] + data['end_date'] + data['number'] + data['detail_number'] + data['sender_name'] \
                      + data['sender_phone'] + data['seller_name'] + data['product_name']

            if not filters:
                raise OrderFilterNotExist('must_be_date_inputs_or_filter_inputs')

            data['page'] = (data['page'] - 1) * data['length']
            if data['sender_phone']:
                data['sender_phone'] = data['sender_phone'].replace("-", "")
            if data['product_name']:
                data['product_name'] = '%' + data['product_name'] + '%'

            return self.master_order_dao.get_order_list_dao(connection, data)

        except KeyError:
            return 'key_error'