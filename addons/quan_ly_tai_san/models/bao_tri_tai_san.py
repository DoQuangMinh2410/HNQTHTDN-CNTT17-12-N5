# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BaoTriTaiSan(models.Model):
    _name = 'bao_tri_tai_san'
    _description = 'Quản lý Bảo trì & Sửa chữa Tài sản'
    _rec_name = 'ma_phieu'
    _order = 'ngay_lap desc'

    ma_phieu = fields.Char("Mã phiếu", required=True, copy=False, default='New')
    tai_san_id = fields.Many2one('tai_san', string="Tài sản", required=True, ondelete='cascade')
    nguoi_yeu_cau_id = fields.Many2one('nhan_vien', string="Người yêu cầu")
    ngay_lap = fields.Date("Ngày lập phiếu", default=fields.Date.today, required=True)
    ngay_du_kien_hoan_thanh = fields.Date("Ngày dự kiến hoàn thành")
    ngay_hoan_thanh = fields.Date("Ngày hoàn thành thực tế")
    
    noi_dung = fields.Text("Nội dung hỏng hóc/bảo trì", required=True)
    chi_phi_sua_chua = fields.Float("Chi phí dự kiến/thực tế (VNĐ)", digits=(16, 0))
    don_vi_sua_chua = fields.Char("Đơn vị / Người sửa chữa")
    
    trang_thai = fields.Selection([
        ('nhap', 'Mới lập'),
        ('dang_sua', 'Đang sửa chữa'),
        ('hoan_thanh', 'Đã hoàn thành'),
        ('huy', 'Hủy bỏ')
    ], string="Trạng thái", default='nhap', required=True)

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            vals['ma_phieu'] = 'BT-' + fields.Datetime.now().strftime('%Y%m%d%H%M%S')
        return super(BaoTriTaiSan, self).create(vals)

    def action_dang_sua(self):
        for rec in self:
            rec.trang_thai = 'dang_sua'

    def action_hoan_thanh(self):
        for rec in self:
            if not rec.chi_phi_sua_chua:
                raise ValidationError("Vui lòng cập nhật Chi phí sửa chữa thực tế trước khi hoàn thành!")
            
            # EVENT-DRIVEN AUTOMATION: KẾ TOÁN
            # Nợ 642 (Chi phí) / Có 1111 (Tiền mặt)
            tk_chi_phi = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '642')], limit=1)
            tk_tien_mat = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '1111')], limit=1)

            if tk_chi_phi and tk_tien_mat:
                but_toan = self.env['but_toan_ke_toan'].create({
                    'dien_giai': f"Chi phí bảo trì tài sản {rec.tai_san_id.ten_tai_san} - Phiếu {rec.ma_phieu}",
                    'tham_chieu': rec.ma_phieu,
                    'nguon_goc': 'he_thong',
                    'chi_tiet_ids': [
                        (0, 0, {
                            'tai_khoan_id': tk_chi_phi.id,
                            'dien_giai': f"Chi phí bảo trì {rec.tai_san_id.ten_tai_san}",
                            'loai': 'no',
                            'so_tien': rec.chi_phi_sua_chua
                        }),
                        (0, 0, {
                            'tai_khoan_id': tk_tien_mat.id,
                            'dien_giai': f"Thanh toán chi phí bảo trì",
                            'loai': 'co',
                            'so_tien': rec.chi_phi_sua_chua
                        })
                    ]
                })
                but_toan.action_ghi_so()

            rec.trang_thai = 'hoan_thanh'
            rec.ngay_hoan_thanh = fields.Date.today()

    def action_huy(self):
        for rec in self:
            rec.trang_thai = 'huy'

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('bao.tri.seq') or 'New'
        return super(BaoTriTaiSan, self).create(vals)
