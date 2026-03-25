# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BaoCaoTaiChinh(models.TransientModel):
    _name = 'bao_cao_tai_chinh'
    _description = 'Báo cáo Kết quả Kinh doanh'

    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng", default=lambda self: str(fields.Date.today().month))
    nam = fields.Integer("Năm", default=lambda self: fields.Date.today().year)

    tong_doanh_thu = fields.Float("Tổng doanh thu", compute='_compute_data', digits=(16, 0))
    tong_chi_phi = fields.Float("Tổng chi phí", compute='_compute_data', digits=(16, 0))
    loi_nhuan = fields.Float("Lợi nhuận ròng", compute='_compute_data', digits=(16, 0))

    def _compute_data(self):
        for rec in self:
            # Lấy tất cả dòng chi tiết bút toán đã ghi sổ trong kỳ
            entries = self.env['chi_tiet_but_toan'].search([
                ('trang_thai', '=', 'da_ghi_so'),
                ('ngay_ghi_so', '>=', f'{rec.nam}-{rec.thang}-01'),
            ])
            
            # Doanh thu: Tài khoản loại 'doanh_thu' (loại 5)
            doanh_thu = sum(entries.filtered(lambda x: x.tai_khoan_id.loai_tai_khoan == 'doanh_thu').mapped(
                lambda x: x.so_tien if x.loai == 'co' else -x.so_tien
            ))
            
            # Chi phí: Tài khoản loại 'chi_phi' (loại 6, 8)
            chi_phi = sum(entries.filtered(lambda x: x.tai_khoan_id.loai_tai_khoan == 'chi_phi').mapped(
                lambda x: x.so_tien if x.loai == 'no' else -x.so_tien
            ))
            
            rec.tong_doanh_thu = doanh_thu
            rec.tong_chi_phi = chi_phi
            rec.loi_nhuan = doanh_thu - chi_phi

    def action_refresh(self):
        # Đây là hàm công khai gọi để kích hoạt tính toán lại nếu cần
        self._compute_data()
        return True

    def action_view_details(self):
        return {
            'name': 'Chi tiết phát sinh',
            'type': 'ir.actions.act_window',
            'res_model': 'chi_tiet_but_toan',
            'view_mode': 'tree,pivot',
            'domain': [
                ('trang_thai', '=', 'da_ghi_so'),
                ('ngay_ghi_so', '>=', f'{self.nam}-{self.thang}-01'),
            ],
        }
