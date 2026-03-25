# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PhepNam(models.Model):
    _name = 'phep_nam'
    _description = 'Quản lý nghỉ phép nhân viên'
    _rec_name = 'display_name'
    _order = 'ngay_bat_dau desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    loai_phep = fields.Selection([
        ('phep_nam', 'Phép năm'),
        ('phep_om', 'Phép ốm'),
        ('phep_thai_san', 'Phép thai sản'),
        ('nghi_le', 'Nghỉ lễ'),
        ('nghi_khong_luong', 'Nghỉ không lương'),
        ('khac', 'Khác'),
    ], string="Loại phép", required=True, default='phep_nam')
    ngay_bat_dau = fields.Date("Từ ngày", required=True, default=fields.Date.today)
    ngay_ket_thuc = fields.Date("Đến ngày", required=True, default=fields.Date.today)
    so_ngay_nghi = fields.Float(
        "Số ngày nghỉ",
        compute='_compute_so_ngay_nghi',
        store=True
    )
    ly_do = fields.Text("Lý do")
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối'),
    ], string="Trạng thái", default='cho_duyet')
    ghi_chu_duyet = fields.Text("Ghi chú duyệt")
    display_name = fields.Char("Tên đơn", compute='_compute_display_name', store=True)

    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_so_ngay_nghi(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.ngay_ket_thuc:
                delta = rec.ngay_ket_thuc - rec.ngay_bat_dau
                rec.so_ngay_nghi = delta.days + 1
            else:
                rec.so_ngay_nghi = 0

    @api.depends('nhan_vien_id', 'loai_phep', 'ngay_bat_dau')
    def _compute_display_name(self):
        loai_map = {
            'phep_nam': 'Phép năm',
            'phep_om': 'Phép ốm',
            'phep_thai_san': 'Thai sản',
            'nghi_le': 'Nghỉ lễ',
            'nghi_khong_luong': 'Không lương',
            'khac': 'Khác',
        }
        for rec in self:
            ten_nv = rec.nhan_vien_id.ho_ten or ''
            loai = loai_map.get(rec.loai_phep, '')
            ngay = str(rec.ngay_bat_dau) if rec.ngay_bat_dau else ''
            rec.display_name = f"{loai} - {ten_nv} ({ngay})"

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay(self):
        for rec in self:
            if rec.ngay_ket_thuc and rec.ngay_bat_dau and rec.ngay_ket_thuc < rec.ngay_bat_dau:
                raise ValidationError("Ngày kết thúc phải sau hoặc bằng ngày bắt đầu!")

    def action_duyet(self):
        for rec in self:
            rec.trang_thai = 'da_duyet'

    def action_tu_choi(self):
        for rec in self:
            rec.trang_thai = 'tu_choi'

    def action_dat_lai(self):
        for rec in self:
            rec.trang_thai = 'cho_duyet'
