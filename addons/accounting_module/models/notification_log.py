# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NotificationLog(models.Model):
    _name = 'notification.log'
    _description = 'Nhật ký Thông báo'
    _rec_name = 'subject'
    _order = 'create_date desc'

    # Basic Information
    subject = fields.Char(string='Tiêu đề', required=True)
    notification_type = fields.Selection(
        [('email', 'Email'),
         ('sms', 'SMS'),
         ('email_sms', 'Email + SMS')],
        string='Loại thông báo',
        required=True
    )

    # Event Information
    event_type = fields.Selection(
        [('depreciation_completed', 'Khấu hao hoàn thành'),
         ('anomaly_detected', 'Phát hiện bất thường'),
         ('asset_expires_soon', 'Tài sản sắp hết niên hạn'),
         ('accounting_error', 'Lỗi ghi nhận kế toán'),
         ('manual', 'Thủ công')],
        string='Loại sự kiện',
        required=True
    )

    # Recipients
    email_to = fields.Char(string='Email đến')
    sms_to = fields.Char(string='Số điện thoại')

    # Content
    subject_line = fields.Char(string='Chủ đề email')
    email_body = fields.Html(string='Nội dung email')
    email_body_text = fields.Text(string='Nội dung email (text)')
    sms_message = fields.Text(string='Nội dung SMS (max 160 ký tự)')

    # Related Records
    asset_id = fields.Many2one(
        'tai_san',
        string='Tài sản'
    )
    depreciation_schedule_id = fields.Many2one(
        'asset.depreciation.schedule',
        string='Lịch khấu hao'
    )
    analysis_id = fields.Many2one(
        'asset.ai.analysis',
        string='Phân tích AI'
    )

    # Status
    status = fields.Selection(
        [('pending', 'Chờ gửi'),
         ('sent', 'Đã gửi'),
         ('failed', 'Lỗi'),
         ('cancelled', 'Hủy')],
        string='Trạng thái',
        default='pending',
        required=True
    )

    # Error Information
    error_message = fields.Text(string='Thông báo lỗi')
    retry_count = fields.Integer(string='Số lần thử lại', default=0)

    # Timestamps
    scheduled_datetime = fields.Datetime(
        string='Thời gian gửi dự kiến',
        default=fields.Datetime.now
    )
    sent_datetime = fields.Datetime(string='Thời gian gửi thực tế')

    # Provider Information
    email_provider = fields.Char(string='Nhà cung cấp email')
    sms_provider = fields.Char(string='Nhà cung cấp SMS')

    # External IDs
    email_external_id = fields.Char(string='Email External ID')
    sms_external_id = fields.Char(string='SMS External ID')

    def action_retry(self):
        """Thử gửi lại thông báo"""
        for record in self:
            if record.status == 'failed':
                record.retry_count += 1
                record.status = 'pending'
                self.env['notification.service'].send_notification(record)

    def action_cancel(self):
        """Hủy thông báo chưa gửi"""
        self.filtered(lambda r: r.status == 'pending').write({'status': 'cancelled'})

    @api.model
    def create_log(self, **kwargs):
        """Tạo log thông báo mới"""
        defaults = {
            'retry_count': 0,
            'status': 'pending',
            'scheduled_datetime': fields.Datetime.now(),
        }
        defaults.update(kwargs)
        return self.create(defaults)

    def log_sent(self, email_external_id=None, sms_external_id=None):
        """Ghi nhận thông báo đã gửi"""
        self.write({
            'status': 'sent',
            'sent_datetime': fields.Datetime.now(),
            'email_external_id': email_external_id,
            'sms_external_id': sms_external_id,
            'error_message': None,
        })

    def log_error(self, error_message):
        """Ghi nhận lỗi gửi"""
        self.write({
            'status': 'failed',
            'error_message': error_message,
        })
