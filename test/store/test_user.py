from unittest import mock, TestCase

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import config
from app import create_app
from utils.connection import get_connection


class TestUser(TestCase):
    """ Test

        Target: store/user_view

        Author: 김민구

        History:
            2020-12-30(김민구): 초기 생성
    """

    def setUp(self):
        self.app = create_app(config.test_config)
        self.connection = get_connection(self.app.config['DB'])
        self.client = self.app.test_client()

        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO permission_types (`id`, `name`) VALUES (3, '일반유저')")
        self.connection.commit()
        self.connection.close()

    def tearDown(self):
        self.connection = get_connection(self.app.config['DB'])
        with self.connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate accounts')
            cursor.execute('truncate users')
            cursor.execute('truncate permission_types')
            cursor.execute('set foreign_key_checks=1')
        self.connection.close()

    def test_user_signup(self):
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
        assert json.loads(response.data)['message'] == 'success'

    def test_user_signup_fail_invalid_data(self):
        data = json.dumps({
            'username': 'br',
            'email': 'brandi@naver.com',
            'phone': '01099998888',
            'password': '1q2w3e$R'
        })

        response = self.client.post(
            '/users/signup',
            data=data,
            content_type='application/json'
        )

        assert response.status_code == 400
        assert json.loads(response.data)['error_message'] == 'username가(이) 유효하지 않습니다.'

    def test_user_signup_fail_duplicate_data(self):
        data = json.dumps({
            'username': 'brandi',
            'email': 'brandi@naver.com',
            'phone': '01099998888',
            'password': '1q2w3e$R'
        })

        data2 = json.dumps({
            'username': 'brandi',
            'email': 'brandi@gmail.com',
            'phone': '01099998888',
            'password': '1q2w3e$R'
        })

        response = self.client.post(
            '/users/signup',
            data=data,
            content_type='application/json'
        )

        assert response.status_code == 200

        response = self.client.post(
            '/users/signup',
            data=data2,
            content_type='application/json'
        )

        assert response.status_code == 403
        assert json.loads(response.data)['error_message'] == '이미 사용중인 username, phone 입니다.'

    def test_user_signin(self):
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
        assert b'token' in response.data

    def test_user_signin_fail_user_not_exist(self):
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
            'username': 'brandi1',
            'password': '1q2w3e$R'
        })
        response = self.client.post(
            '/users/signin',
            data=signin_data,
            content_type='application/json'
        )

        assert response.status_code == 403
        assert b'token' not in response.data
        assert json.loads(response.data)['error_message'] == '로그인에 실패했습니다.'

    def test_user_signin_fail_user_wrong_password(self):
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
            'password': '1q2w3e$'
        })
        response = self.client.post(
            '/users/signin',
            data=signin_data,
            content_type='application/json'
        )

        assert response.status_code == 403
        assert b'token' not in response.data
        assert json.loads(response.data)['error_message'] == '로그인에 실패했습니다.'

    @mock.patch('view.store.user_view.id_token')
    def test_social_sign_in(self, mock_id_token):
        """ POST 메소드: 유저 구글 소셜 로그인

            Decorator: 가짜 구글 라이브러리 함수를 만들기 위한 mock.patch 데코레이터

            Args: 가짜 구글 라이브러리 함수

            Author: 김민구

            Return:
                True: response.status_code == 200 : 유저 로그인 성공 status_code
                True: b'token' in response.data   : 유저 로그인 성공 토큰 확인 여부

            History:
                2020-12-30(김민구): 초기 생성

            Notes:
                소셜 로그인 구조상 Integration Test를 하기 힘들기 때문에 간략하게 성공 케이스를 확인하는 용도로 작성
                토큰, 토큰을 확인하는 구글 라이브러리 함수를 mocking으로 사용해 테스트 진행
                구글 라이브러리 함수의 리턴 값은 이메일이 담겨있는 딕셔너리 (소셜 로그인시 이메일만 필요하기 때문)
        """

        mock_id_token.verify_oauth2_token.return_value = {
             "email": "test_user@gmail.com"
        }
        response = self.client.post(
            '/users/social-signin',
            headers={'Authorization': 'google_token'}
        )
        assert response.status_code == 200
        assert b'token' in response.data

    @mock.patch('view.store.user_view.id_token')
    def test_social_signin_fail_no_token(self, mock_id_token):

        mock_id_token.verify_oauth2_token.return_value = {
            "name": "test_user@gmail.com"
        }
        response = self.client.post(
            '/users/social-signin',
            headers={'Authorization': 'google_token'}
        )

        assert response.status_code == 403
        assert json.loads(response.data)['error_message'] == '구글 소셜 로그인에 실패하였습니다.'
