# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import json

try:
    from google.auth.transport.requests import Request
    from google.oauth2.service_account import Credentials
    import base64
except ImportError:
    pass


class NotifyEmailConfig(models.Model):
    _name = 'notify.email.config'
    _description = 'Cấu hình Gửi Email thông báo'
    _rec_name = 'name'

    name = fields.Char(string='Tên Cấu hình', required=True)
    is_active = fields.Boolean(string='Kích hoạt', default=True)
    email_provider = fields.Selection(
        [('gmail', 'Gmail API'),
         ('smtp', 'SMTP Server'),
         ('sendgrid', 'SendGrid API')],
        string='Nhà cung cấp Email',
        default='gmail'
    )

    # Gmail Configuration
    gmail_service_account_json = fields.Text(
        string='Gmail Service Account JSON',
        help='Dán nội dung file JSON từ Google Cloud Console'
    )
    gmail_sender_email = fields.Char(
        string='Email gửi từ',
        help='Địa chỉ email sẽ được sử dụng để gửi thông báo'
    )

    # SMTP Configuration
    smtp_host = fields.Char(string='SMTP Host')
    smtp_port = fields.Integer(string='SMTP Port', default=587)
    smtp_username = fields.Char(string='Username')
    smtp_password = fields.Char(string='Password', widget='password')
    smtp_use_tls = fields.Boolean(string='Sử dụng TLS', default=True)

    # SendGrid Configuration
    sendgrid_api_key = fields.Char(string='SendGrid API Key', widget='password')
    sendgrid_sender_email = fields.Char(string='SendGrid Sender Email')

    # General Settings
    sender_name = fields.Char(string='Tên người gửi', default='Hệ thống Quản lý Tài sản')
    reply_to_email = fields.Char(string='Email trả lời')
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
            if record.email_provider == 'gmail':
                record.is_configured = bool(
                    record.gmail_service_account_json and
                    record.gmail_sender_email
                )
            elif record.email_provider == 'smtp':
                record.is_configured = bool(
                    record.smtp_host and
                    record.smtp_username and
                    record.smtp_password
                )
            elif record.email_provider == 'sendgrid':
                record.is_configured = bool(
                    record.sendgrid_api_key and
                    record.sendgrid_sender_email
                )
            else:
                record.is_configured = False

    def action_test_connection(self):
        """Kiểm tra kết nối email"""
        for record in self:
            try:
                if record.email_provider == 'gmail':
                    record._test_gmail_connection()
                elif record.email_provider == 'smtp':
                    record._test_smtp_connection()
                elif record.email_provider == 'sendgrid':
                    record._test_sendgrid_connection()
                else:
                    raise ValidationError('Nhà cung cấp email không xác định')

                record.test_status = 'success'
                record.test_message = '✅ Kết nối thành công'
                record.last_test = fields.Datetime.now()

            except Exception as e:
                record.test_status = 'error'
                record.test_message = f'❌ Lỗi: {str(e)}'
                record.last_test = fields.Datetime.now()

    def _test_gmail_connection(self):
        """Test Gmail API connection"""
        if not self.gmail_service_account_json:
            raise ValidationError('Vui lòng nhập Gmail Service Account JSON')
        
        try:
            json.loads(self.gmail_service_account_json)
        except json.JSONDecodeError:
            raise ValidationError('JSON không hợp lệ')

    def _test_smtp_connection(self):
        """Test SMTP connection"""
        import smtplib
        
        if not all([self.smtp_host, self.smtp_username, self.smtp_password]):
            raise ValidationError('Vui lòng điền đầy đủ thông tin SMTP')

        try:
            if self.smtp_use_tls:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            
            server.login(self.smtp_username, self.smtp_password)
            server.quit()
        except Exception as e:
            raise ValidationError(f'Không thể kết nối SMTP: {str(e)}')

    def _test_sendgrid_connection(self):
        """Test SendGrid API connection"""
        import requests

        if not self.sendgrid_api_key:
            raise ValidationError('Vui lòng nhập SendGrid API Key')

        try:
            headers = {
                'Authorization': f'Bearer {self.sendgrid_api_key}',
                'Content-Type': 'application/json'
            }
            response = requests.get(
                'https://api.sendgrid.com/v3/stats',
                headers=headers,
                timeout=5
            )
            if response.status_code != 200:
                raise ValidationError(f'SendGrid API trả về: {response.status_code}')
        except Exception as e:
            raise ValidationError(f'Lỗi SendGrid: {str(e)}')

    @staticmethod
    def get_active_config():
        """Lấy cấu hình email hoạt động"""
        config = NotifyEmailConfig.search([
            ('is_active', '=', True),
            ('is_configured', '=', True)
        ], limit=1)
        
        if not config:
            raise ValidationError(
                'Chưa có cấu hình Email hoạt động. '
                'Vui lòng kiểm tra trong Accounting → Cấu hình Email Thông báo'
            )
        return config[0]
