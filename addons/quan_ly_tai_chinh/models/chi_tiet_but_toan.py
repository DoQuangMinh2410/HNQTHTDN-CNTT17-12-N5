# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ChiTietButToan(models.Model):
    _name = 'chi_tiet_but_toan'
    _description = 'Chi tiết Bút toán (Journal Item)'
    _rec_name = 'dien_giai'

    but_toan_id = fields.Many2one('but_toan_ke_toan', string="Bút toán", required=True, ondelete='cascade')
    tai_khoan_id = fields.Many2one('tai_khoan_ke_toan', string="Tài khoản", required=True, ondelete='restrict')
    doi_tuong = fields.Char("Đối tượng (Khách hàng/Nhân viên/Tài sản)")
    dien_giai = fields.Char("Diễn giải chi tiết")
    loai = fields.Selection([
        ('no', 'Nợ'),
        ('co', 'Có'),
    ], string="Nợ/Có", required=True)
    so_tien = fields.Float("Số tiền (VNĐ)", required=True, digits=(16, 0))

    ngay_ghi_so = fields.Date(related='but_toan_id.ngay_ghi_so', store=True)
    trang_thai = fields.Selection(related='but_toan_id.trang_thai', store=True)

    @api.onchange('but_toan_id')
    def _onchange_but_toan(self):
        if self.but_toan_id and not self.dien_giai:
            self.dien_giai = self.but_toan_id.dien_giai
