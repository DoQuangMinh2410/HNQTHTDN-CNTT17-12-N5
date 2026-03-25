# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TaiKhoanKeToan(models.Model):
    _name = 'tai_khoan_ke_toan'
    _description = 'Tài Khoản Kế Toán (Sổ Cái)'
    _rec_name = 'display_name'
    _order = 'ma_tai_khoan asc'

    ma_tai_khoan = fields.Char("Mã tài khoản", required=True)
    ten_tai_khoan = fields.Char("Tên tài khoản", required=True)
    loai_tai_khoan = fields.Selection([
        ('tai_san', 'Tài sản'),
        ('nguon_von', 'Nguồn vốn'),
        ('von_chu_so_huu', 'Vốn chủ sở hữu'),
        ('doanh_thu', 'Doanh thu'),
        ('chi_phi', 'Chi phí'),
    ], string="Loại tài khoản", required=True)
    
    chi_tiet_ids = fields.One2many('chi_tiet_but_toan', 'tai_khoan_id', string="Chi tiết phát sinh")
    so_du = fields.Float("Số dư hiện tại", compute='_compute_so_du', store=True, digits=(16, 0))
    display_name = fields.Char("Hiển thị", compute='_compute_display_name', store=True)

    @api.depends('ma_tai_khoan', 'ten_tai_khoan')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.ma_tai_khoan} - {rec.ten_tai_khoan}"

    @api.depends('chi_tiet_ids.so_tien', 'chi_tiet_ids.loai')
    def _compute_so_du(self):
        for rec in self:
            tong_no = sum(rec.chi_tiet_ids.filtered(lambda x: x.loai == 'no').mapped('so_tien'))
            tong_co = sum(rec.chi_tiet_ids.filtered(lambda x: x.loai == 'co').mapped('so_tien'))
            if rec.loai_tai_khoan in ['tai_san', 'chi_phi']:
                rec.so_du = tong_no - tong_co
            else:
                rec.so_du = tong_co - tong_no
