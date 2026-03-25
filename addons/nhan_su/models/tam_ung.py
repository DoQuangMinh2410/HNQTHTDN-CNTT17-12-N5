# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TamUng(models.Model):
    _name = 'tam_ung_nhan_vien'
    _description = 'Quản lý Tạm ứng Nhân viên'
    _rec_name = 'ma_tam_ung'
    _order = 'ngay_tam_ung desc'

    ma_tam_ung = fields.Char("Mã tạm ứng", required=True, copy=False, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay_tam_ung = fields.Date("Ngày tạm ứng", default=fields.Date.today, required=True)
    so_tien = fields.Float("Số tiền tạm ứng (VNĐ)", digits=(16, 0), required=True)
    ly_do = fields.Text("Lý do tạm ứng", required=True)
    
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt (Chờ chi)'),
        ('da_chi', 'Đã chi tiền'),
        ('da_hoan_ung', 'Đã hoàn ứng/Kết thúc'),
    ], string="Trạng thái", default='nhap')

    but_toan_id = fields.Many2one('but_toan_ke_toan', string="Bút toán kế toán", readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('ma_tam_ung', 'New') == 'New':
            vals['ma_tam_ung'] = self.env['ir.sequence'].next_by_code('tam.ung.seq') or 'New'
        return super(TamUng, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.trang_thai = 'cho_duyet'

    def action_approve(self):
        for rec in self:
            rec.trang_thai = 'da_duyet'

    def action_pay(self):
        for rec in self:
            # Tự động sinh bút toán Nợ 141 (Tạm ứng) / Có 111 (Tiền mặt)
            tk_tam_ung = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '141')], limit=1)
            tk_tien_mat = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '111')], limit=1)
            
            if not tk_tam_ung or not tk_tien_mat:
                raise ValidationError("Vui lòng cấu hình tài khoản 141 (Tạm ứng) và 111 (Tiền mặt) trước!")

            but_toan = self.env['but_toan_ke_toan'].create({
                'dien_giai': f'Chi tạm ứng cho {rec.nhan_vien_id.ho_ten} - {rec.ma_tam_ung}',
                'tham_chieu': rec.ma_tam_ung,
                'nguon_goc': 'he_thong',
                'chi_tiet_ids': [
                    (0, 0, {
                        'tai_khoan_id': tk_tam_ung.id,
                        'doi_tuong': rec.nhan_vien_id.ho_ten,
                        'dien_giai': 'Tạm ứng cho nhân viên',
                        'loai': 'no',
                        'so_tien': rec.so_tien
                    }),
                    (0, 0, {
                        'tai_khoan_id': tk_tien_mat.id,
                        'doi_tuong': rec.nhan_vien_id.ho_ten,
                        'dien_giai': 'Chi tiền mặt tạm ứng',
                        'loai': 'co',
                        'so_tien': rec.so_tien
                    })
                ]
            })
            rec.write({
                'trang_thai': 'da_chi',
                'but_toan_id': but_toan.id
            })

    def action_done(self):
        for rec in self:
            rec.trang_thai = 'da_hoan_ung'
