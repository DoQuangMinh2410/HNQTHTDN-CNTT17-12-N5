# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ChamCong(models.Model):
    _name = 'cham_cong'
    _description = 'Chấm công nhân viên'
    _rec_name = 'display_name'
    _order = 'nam desc, thang desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng", required=True)
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)
    so_ngay_cong_chuan = fields.Float("Ngày công chuẩn", default=26.0)
    so_ngay_cong_thuc_te = fields.Float("Ngày công thực tế")
    so_ngay_nghi_phep = fields.Float("Ngày nghỉ phép")
    so_ngay_nghi_le = fields.Float("Ngày nghỉ lễ")
    so_ngay_nghi_khong_luong = fields.Float("Nghỉ không lương")
    so_gio_lam_them = fields.Float("Số giờ làm thêm")
    he_so_cong = fields.Float(
        "Hệ số công",
        compute='_compute_he_so_cong',
        store=True,
        digits=(10, 4)
    )
    display_name = fields.Char(
        "Kỳ chấm công",
        compute='_compute_display_name',
        store=True
    )
    ghi_chu = fields.Text("Ghi chú")

    @api.depends('so_ngay_cong_thuc_te', 'so_ngay_cong_chuan')
    def _compute_he_so_cong(self):
        for rec in self:
            if rec.so_ngay_cong_chuan and rec.so_ngay_cong_chuan > 0:
                rec.he_so_cong = rec.so_ngay_cong_thuc_te / rec.so_ngay_cong_chuan
            else:
                rec.he_so_cong = 0.0

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_display_name(self):
        for rec in self:
            ten_nv = rec.nhan_vien_id.ho_ten or ''
            rec.display_name = f"CC {ten_nv} - T{rec.thang}/{rec.nam}"

    @api.constrains('thang', 'nam', 'nhan_vien_id')
    def _check_unique(self):
        for rec in self:
            domain = [
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('thang', '=', rec.thang),
                ('nam', '=', rec.nam),
                ('id', '!=', rec.id),
            ]
            if self.search_count(domain) > 0:
                raise ValidationError("Đã tồn tại bảng chấm công cho nhân viên này trong kỳ đã chọn!")
