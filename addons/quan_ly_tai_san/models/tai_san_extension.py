# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class TaiSanExtension(models.Model):
    """Mở rộng model tai_san để liên kết với nhân viên"""
    _inherit = 'tai_san'

    # Liên kết với nhân viên
    phan_bo_employee_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên được giao',
        help='Nhân viên được giao tài sản này'
    )
    
    assignment_date = fields.Date('Ngày gán cho nhân viên')
    
    # Không gắn chặt module kế toán trên module tài sản để tránh phụ thuộc vòng
    # Kết nối khấu hao và bút toán sẽ được khai báo trong accounting_module.
    
    # Trạng thái sử dụng (thay cho trang_thai_thanh_ly)
    usage_status = fields.Selection([
        ('draft', 'Nháp'),
        ('in_use', 'Đang sử dụng'),
        ('broken', 'Hư hỏng'),
        ('disposed', 'Đã thanh lý'),
    ], string='Trạng thái sử dụng', default='draft')

    def action_confirm(self):
        """Xác nhận tài sản."""
        for record in self:
            if record.usage_status != 'draft':
                continue
            record.usage_status = 'in_use'
            # Phần khấu hao kế toán sẽ được thực hiện trong accounting_module nếu cài đặt.
            return True

    # def action_assign_employee(self):
    #     """Gán tài sản cho nhân viên"""
    #     if not self.phan_bo_employee_id:
    #         raise models.ValidationError("Vui lòng chọn nhân viên!")
        
    #     self.assignment_date = datetime.now().date()
        
    #     # Tạo record gán tài sản
    #     AssetAssignment = self.env['asset.assignment']
    #     AssetAssignment.create({
    #         'asset_id': self.id,
    #         'employee_id': self.phan_bo_employee_id.id,
    #         'assignment_date': self.assignment_date,
    #     })

    def action_depreciate(self):
        """Tạo khấu hao ngay lập tức"""
        if self.pp_khau_hao == 'none':
            raise models.ValidationError("Tài sản này không có phương pháp khấu hao!")
        
        # Lấy lịch khấu hao hiện tại
        if self.depreciation_schedule_id:
            self.depreciation_schedule_id.action_generate_depreciation()
        else:
            # Tạo khấu hao theo phương thức cũ
            self.action_tinh_khau_hao()

    # @api.model
    # def schedule_monthly_depreciation(self):
    #     """Scheduled Job - chạy hàng tháng để tạo khấu hao"""
    #     assets = self.search([
    #         ('usage_status', '=', 'in_use'),
    #         ('pp_khau_hao', '!=', 'none'),
    #         ('depreciation_schedule_id', '!=', False),
    #     ])
        
    #     for asset in assets:
    #         # Kiểm tra xem khấu hao tháng này đã tạo chưa
    #         current_month = datetime.now().strftime('%m/%Y')
    #         existing = asset.depreciation_ids.filtered(lambda r: r.month == current_month)
            
    #         if not existing and asset.depreciation_schedule_id:
    #             asset.depreciation_schedule_id.action_generate_depreciation()
