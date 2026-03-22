# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests


class NotifySmsConfig(models.Model):
    _name = 'notify.sms.config'
    _description = 'Cấu hình Gửi SMS thông báo'
    _rec_name = 'name'

    name = fields.Char(string='Tên Cấu hình', required=True)
    is_active = fields.Boolean(string='Kích hoạt', default=True)
    sms_provider = fields.Selection(
        [('viettel', 'Viettel SMS API'),
         ('twilio', 'Twilio'),
         ('aws_sns', 'AWS SNS')],
        string='Nhà cung cấp SMS',
        default='viettel'
    )

    # Viettel Configuration
    viettel_api_url = fields.Char(
        string='Viettel API URL',
        default='https://api.viettel.com.vn/sms/send'
    )
    viettel_cp_code = fields.Char(
        string='Viettel CP Code',
        help='Mã CP được cấp từ Viettel'
    )
    viettel_username = fields.Char(
        string='Username',
        help='Tên đăng nhập Viettel'
    )
    viettel_password = fields.Char(
        string='Password',
        widget='password',
        help='Mật khẩu Viettel'
    )
    viettel_sender = fields.Char(
        string='Sender ID',
        default='SYSTEM',
        help='ID người gửi (hiển thị trên điện thoại)'
    )

    # Twilio Configuration
    twilio_account_sid = fields.Char(
        string='Twilio Account SID',
        widget='password'
    )
    twilio_auth_token = fields.Char(
        string='Twilio Auth Token',
        widget='password'
    )
    twilio_phone_number = fields.Char(
        string='Twilio Phone Number',
        help='Số điện thoại Twilio (định dạng: +1234567890)'
    )

    # AWS SNS Configuration
    aws_access_key = fields.Char(
        string='AWS Access Key',
        widget='password'
    )
    aws_secret_key = fields.Char(
        string='AWS Secret Key',
        widget='password'
    )
    aws_region = fields.Char(
        string='AWS Region',
        default='ap-southeast-1'
    )

    # General Settings
    message_encoding = fields.Selection(
        [('utf8', 'UTF-8'),
         ('unicode', 'Unicode'),
         ('gsm7', 'GSM 7-bit')],
        string='Mã hóa tin nhắn',
        default='utf8'
    )
    is_configured = fields.Boolean(
        string='Đã cấu hình',
        compute='_compute_is_configured',
        store=False
    )

    # Test Results
    test_status = fields.Selection(
        [('pending', 'Chưa kiểm tra'),
         ('success', 'Thành công'),
         ('error', 'Lỗi')],
        string='Trạng thái kiểm tra',
        default='pending',
        readonly=True
    )
    test_message = fields.Text(
        string='Chi tiết kiểm tra',
        readonly=True
    )
    last_test = fields.Datetime(
        string='Lần kiểm tra cuối',
        readonly=True
    )

    def _compute_is_configured(self):
        """Kiểm tra xem cấu hình đã đúng chưa"""
        for record in self:
            if record.sms_provider == 'viettel':
                record.is_configured = bool(
                    record.viettel_cp_code and
                    record.viettel_username and
                    record.viettel_password
                )
            elif record.sms_provider == 'twilio':
                record.is_configured = bool(
                    record.twilio_account_sid and
                    record.twilio_auth_token and
                    record.twilio_phone_number
                )
            elif record.sms_provider == 'aws_sns':
                record.is_configured = bool(
                    record.aws_access_key and
                    record.aws_secret_key
                )
            else:
                record.is_configured = False

    def action_test_connection(self):
        """Kiểm tra kết nối SMS"""
        for record in self:
            try:
                if record.sms_provider == 'viettel':
                    record._test_viettel_connection()
                elif record.sms_provider == 'twilio':
                    record._test_twilio_connection()
                elif record.sms_provider == 'aws_sns':
                    record._test_aws_sns_connection()
                else:
                    raise ValidationError('Nhà cung cấp SMS không xác định')

                record.test_status = 'success'
                record.test_message = '✅ Kết nối thành công'
                record.last_test = fields.Datetime.now()

            except Exception as e:
                record.test_status = 'error'
                record.test_message = f'❌ Lỗi: {str(e)}'
                record.last_test = fields.Datetime.now()

    def _test_viettel_connection(self):
        """Test Viettel SMS API connection"""
        if not all([self.viettel_cp_code, self.viettel_username, self.viettel_password]):
            raise ValidationError('Vui lòng điền đầy đủ thông tin Viettel')

        try:
            response = requests.post(
                self.viettel_api_url,
                json={
                    'cpCode': self.viettel_cp_code,
                    'username': self.viettel_username,
                    'password': self.viettel_password,
                    'senderID': self.viettel_sender,
                    'receiver': '+84999999999',  # Số test
                    'message': 'Test ket noi'
                },
                timeout=10
            )
            
            if response.status_code not in [200, 201]:
                raise ValidationError(
                    f'Viettel API trả về: {response.status_code} - {response.text[:100]}'
                )
        except requests.RequestException as e:
            raise ValidationError(f'Lỗi kết nối Viettel: {str(e)}')

    def _test_twilio_connection(self):
        """Test Twilio connection"""
        try:
            from twilio.rest import Client
        except ImportError:
            raise ValidationError('Vui lòng cài đặt thư viện twilio: pip install twilio')

        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
            raise ValidationError('Vui lòng điền đầy đủ thông tin Twilio')

        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            # Just validate credentials
            client.api.accounts(self.twilio_account_sid).fetch()
        except Exception as e:
            raise ValidationError(f'Lỗi Twilio: {str(e)}')

    def _test_aws_sns_connection(self):
        """Test AWS SNS connection"""
        try:
            import boto3
        except ImportError:
            raise ValidationError('Vui lòng cài đặt thư viện boto3: pip install boto3')

        if not all([self.aws_access_key, self.aws_secret_key]):
            raise ValidationError('Vui lòng điền đầy đủ thông tin AWS')

        try:
            session = boto3.Session(
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            sns = session.client('sns')
            sns.list_topics()  # Test call
        except Exception as e:
            raise ValidationError(f'Lỗi AWS SNS: {str(e)}')

    @staticmethod
    def get_active_config():
        """Lấy cấu hình SMS hoạt động"""
        config = NotifySmsConfig.search([
            ('is_active', '=', True),
            ('is_configured', '=', True)
        ], limit=1)
        
        if not config:
            raise ValidationError(
                'Chưa có cấu hình SMS hoạt động. '
                'Vui lòng kiểm tra trong Accounting → Cấu hình SMS Thông báo'
            )
        return config[0]
