# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta


class AssetDepreciationSchedule(models.Model):
    _name = 'asset.depreciation.schedule'
    _description = 'Lịch khấu hao tài sản'
    _rec_name = 'asset_id'

    asset_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    
    # Thông tin khấu hao
    original_value = fields.Float('Giá trị ban đầu', required=True)
    depreciation_method = fields.Selection([
        ('straight_line', 'Tuyến tính'),
        ('degressive', 'Giảm dần'),
    ], string='Phương pháp khấu hao', default='straight_line')
    
    # Thời gian sử dụng (tháng)
    useful_life_months = fields.Integer('Thời gian sử dụng (tháng)', required=True, default=60)
    
    # Tỷ lệ khấu hao (cho degressive)
    annual_rate = fields.Float('Tỷ lệ khấu hao hàng năm (%)', default=20)
    
    # Ngày bắt đầu
    start_date = fields.Date('Ngày bắt đầu', required=True, default=fields.Date.today)
    
    # Tính toán tự động
    monthly_depreciation = fields.Float('Khấu hao tháng (tuyến tính)', compute='_compute_monthly_depreciation', store=True)
    total_depreciation_periods = fields.Integer('Số kỳ khấu hao', compute='_compute_total_periods', store=True)

    # Trạng thái lịch
    is_active = fields.Boolean('Đang hoạt động', default=True)

    @api.depends('original_value', 'useful_life_months')
    def _compute_monthly_depreciation(self):
        """Tính khấu hao tuyến tính hàng tháng"""
        for record in self:
            if record.useful_life_months > 0:
                record.monthly_depreciation = record.original_value / record.useful_life_months
            else:
                record.monthly_depreciation = 0

    @api.depends('useful_life_months')
    def _compute_total_periods(self):
        """Tính tổng số kỳ khấu hao"""
        for record in self:
            record.total_depreciation_periods = record.useful_life_months

    def action_generate_depreciation(self):
        """Tạo lịch khấu hao hàng tháng"""
        Depreciation = self.env['asset.depreciation']
        LichSuKhauHao = self.env['lich_su_khau_hao']

        for record in self:
            if not record.is_active:
                continue

            # Kiểm tra khấu hao đã tạo
            existing = Depreciation.search([('asset_id', '=', record.asset_id.id)])
            asset = record.asset_id

            # Tạo khấu hao cho các tháng chưa có
            current_date = record.start_date
            for i in range(record.total_depreciation_periods):
                month_key = current_date.strftime('%m/%Y')

                # Kiểm tra xem tháng này đã tạo chưa
                month_exists = existing.filtered(lambda r: r.month == month_key)

                if month_exists:
                    current_date += relativedelta(months=1)
                    continue

                if asset.gia_tri_hien_tai <= 0:
                    break

                depreciation = Depreciation.create({
                    'asset_id': asset.id,
                    'original_value': record.original_value,
                    'depreciation_amount': record.monthly_depreciation,
                    'depreciation_method': record.depreciation_method,
                    'date': current_date,
                })
                existing |= depreciation

                # Đồng bộ với model tài sản gốc
                asset.write({
                    'gia_tri_hien_tai': max(0.0, asset.gia_tri_hien_tai - depreciation.depreciation_amount),
                    'thoi_gian_su_dung': asset.thoi_gian_su_dung + 1,
                })

                # Ghi lại lịch sử khấu hao (legacy) mà không trừ thêm giá trị tài sản nữa
                LichSuKhauHao.with_context(skip_asset_update=True).create({
                    'ma_phieu_khau_hao': f"KH-{asset.ma_tai_san}-{current_date.strftime('%Y%m%d%H%M%S')}",
                    'ma_ts': asset.id,
                    'ngay_khau_hao': fields.Datetime.to_string(datetime.combine(current_date, datetime.min.time())),
                    'so_tien_khau_hao': depreciation.depreciation_amount,
                    'loai_phieu': 'automatic',
                    'ghi_chu': f'Khấu hao lịch trình {month_key}',
                })

                current_date += relativedelta(months=1)

            # Gửi thông báo khấu hao hoàn thành
            self._send_completion_notification(record)

    def _send_completion_notification(self, record):
        """Gửi thông báo khi khấu hao hoàn thành"""
        try:
            # Kiểm tra cấu hình thông báo
            email_configs = self.env['notify.email.config'].search([('is_active', '=', True)])
            sms_configs = self.env['notify.sms.config'].search([('is_active', '=', True)])
            
            if not (email_configs or sms_configs):
                return  # Không cấu hình thông báo
            
            # Lấy danh sách nhận thông báo từ asset
            recipients = self._get_notification_recipients(record.asset_id)
            
            if not recipients:
                return
            
            # Tạo log thông báo
            notification_type = 'email_sms' if (email_configs and sms_configs) else ('email' if email_configs else 'sms')
            
            for recipient in recipients:
                asset_name = record.asset_id.cus_rec_name or record.asset_id.ten_tai_san or str(record.asset_id.id)
                email_body_text = f"""
Khấu hao Tài sản: {asset_name}

Chi tiết:
- Tên tài sản: {asset_name}
- Giá trị khấu hao hàng tháng: {record.monthly_depreciation:,.0f} VND
- Phương pháp: {dict(self._fields['depreciation_method'].selection).get(record.depreciation_method, record.depreciation_method)}
- Thời gian sử dụng: {record.useful_life_months} tháng
- Số kỳ khấu hao: {record.total_depreciation_periods} kỳ

Lịch khấu hao đã được tạo thành công.
Vui lòng kiểm tra chi tiết trong hệ thống.
"""
                
                notification_log = self.env['notification.log'].create_log(
                    subject=f'✓ Khấu hao tài sản: {record.asset_id.name}',
                    event_type='depreciation_completed',
                    notification_type=notification_type,
                    email_to=recipient.get('email'),
                    sms_to=recipient.get('phone'),
                    subject_line=f'Khấu hao: {record.asset_id.name}',
                    email_body_text=email_body_text,
                    sms_message=f"✓ Khấu hao {record.asset_id.name[:20]} hoàn thành. {record.total_depreciation_periods} kỳ.",
                    depreciation_schedule_id=record.id,
                    asset_id=record.asset_id.id,
                    email_provider=email_configs[0].email_provider if email_configs else None,
                    sms_provider=sms_configs[0].sms_provider if sms_configs else None,
                )
                
                # Gửi thông báo
                self.env['notification.service'].send_notification(notification_log)
        except Exception as e:
            self.env['notification.log'].create_log(
                subject=f'❌ Lỗi gửi thông báo: {str(e)[:50]}',
                event_type='depreciation_completed',
                notification_type='email',
                error_message=str(e)
            )

    def _get_notification_recipients(self, asset):
        """Lấy danh sách nhận thông báo từ asset"""
        recipients = []
        
        # Kiểm tra fields liên quan người dùng/người quản lý trong Asset model
        # Bạn có thể customize danh sách này căn cứ vào logic công ty
        
        # Ví dụ: Lấy từ user hoặc department của asset
        if hasattr(asset, 'manager_id') and asset.manager_id:
            if asset.manager_id.email:
                recipients.append({
                    'email': asset.manager_id.email,
                    'phone': getattr(asset.manager_id, 'mobile', None)
                })
        
        # Hoặc lấy từ danh sách cấu hình mặc định
        if not recipients:
            config_users = self.env['res.users'].search([('groups_id', '=', self.env.ref('base.group_system').id)])
            for user in config_users[:3]:  # Top 3 system users
                if user.email:
                    recipients.append({
                        'email': user.email,
                        'phone': getattr(user, 'mobile', None)
                    })
        
        return recipients
