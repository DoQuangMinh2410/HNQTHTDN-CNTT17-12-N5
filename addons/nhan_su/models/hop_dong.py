# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HopDong(models.Model):
    _name = 'hop_dong'
    _description = 'Hợp đồng lao động'
    _rec_name = 'ma_hop_dong'
    _order = 'ngay_bat_dau desc'

    ma_hop_dong = fields.Char("Mã hợp đồng", required=True, copy=False, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('xac_dinh_thoi_han', 'Xác định thời hạn'),
        ('khong_xac_dinh_thoi_han', 'Không xác định thời hạn'),
    ], string="Loại hợp đồng", required=True, default='xac_dinh_thoi_han')
    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True, default=fields.Date.today)
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    luong_co_ban = fields.Float("Lương cơ bản (VNĐ)", digits=(16, 0), required=True)
    he_so_luong = fields.Float("Hệ số lương", default=1.0)
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('hieu_luc', 'Đang hiệu lực'),
        ('het_han', 'Hết hạn'),
        ('cham_dut', 'Đã chấm dứt'),
    ], string="Trạng thái", compute='_compute_trang_thai', store=True)
    ghi_chu = fields.Text("Ghi chú")

    @api.depends('ngay_bat_dau', 'ngay_ket_thuc', 'loai_hop_dong')
    def _compute_trang_thai(self):
        today = fields.Date.today()
        for rec in self:
            if not rec.ngay_bat_dau:
                rec.trang_thai = 'nhap'
            elif rec.ngay_bat_dau > today:
                rec.trang_thai = 'nhap'
            elif rec.loai_hop_dong == 'khong_xac_dinh_thoi_han':
                rec.trang_thai = 'hieu_luc'
            elif rec.ngay_ket_thuc and rec.ngay_ket_thuc < today:
                rec.trang_thai = 'het_han'
            else:
                rec.trang_thai = 'hieu_luc'

    def action_cham_dut(self):
        for rec in self:
            rec.trang_thai = 'cham_dut'

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.ngay_ket_thuc and rec.ngay_ket_thuc < rec.ngay_bat_dau:
                raise ValidationError("Ngày kết thúc phải sau ngày bắt đầu!")

    @api.model
    def create(self, vals):
        if vals.get('ma_hop_dong', 'New') == 'New':
            vals['ma_hop_dong'] = self.env['ir.sequence'].next_by_code('hop.dong.seq') or 'New'
        return super(HopDong, self).create(vals)
