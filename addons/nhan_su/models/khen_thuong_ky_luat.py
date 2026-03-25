# -*- coding: utf-8 -*-
from odoo import models, fields, api


class KhenThuongKyLuat(models.Model):
    _name = 'khen_thuong_ky_luat'
    _description = 'Khen thưởng và kỷ luật nhân viên'
    _rec_name = 'so_quyet_dinh'
    _order = 'ngay_quyet_dinh desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    loai = fields.Selection([
        ('khen_thuong', 'Khen thưởng'),
        ('ky_luat', 'Kỷ luật'),
    ], string="Loại", required=True, default='khen_thuong')
    hinh_thuc = fields.Selection([
        # Khen thưởng
        ('khen_mien', 'Khen miệng / Email'),
        ('bang_khen', 'Bằng khen / Giấy khen'),
        ('tang_thuong', 'Tặng thưởng tiền mặt'),
        ('len_luong', 'Thăng cấp / Tăng lương'),
        # Kỷ luật
        ('nhac_nho', 'Nhắc nhở'),
        ('khien_trach', 'Khiển trách'),
        ('canh_cao', 'Cảnh cáo'),
        ('ha_bac_luong', 'Hạ bậc lương'),
        ('dieu_chuyen', 'Điều chuyển vị trí'),
        ('tam_dinh_chi', 'Tạm đình chỉ công tác'),
        ('sa_thai', 'Sa thải'),
    ], string="Hình thức")
    ngay_quyet_dinh = fields.Date("Ngày quyết định", required=True, default=fields.Date.today)
    so_quyet_dinh = fields.Char("Số quyết định", required=True)
    ly_do = fields.Text("Lý do / Mô tả")
    gia_tri_thuong_phat = fields.Float("Giá trị thưởng/phạt (VNĐ)", digits=(16, 0),
                                       help="Số tiền thưởng (dương) hoặc phạt (âm nếu khấu trừ)")
    nguoi_ky_quyet_dinh = fields.Char("Người ký quyết định")
    file_quyet_dinh = fields.Binary("File quyết định", attachment=True)
    file_quyet_dinh_name = fields.Char("Tên file")
    ghi_chu = fields.Text("Ghi chú bổ sung")

    @api.onchange('loai')
    def _onchange_loai(self):
        """Reset hình thức khi đổi loại"""
        self.hinh_thuc = False
