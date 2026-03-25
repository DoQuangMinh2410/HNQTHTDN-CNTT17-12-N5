# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TinhLuong(models.Model):
    _name = 'tinh_luong'
    _description = 'Bảng tính lương nhân viên'
    _rec_name = 'display_name'
    _order = 'nam desc, thang desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    hop_dong_id = fields.Many2one('hop_dong', string="Hợp đồng", domain="[('nhan_vien_id','=',nhan_vien_id)]")
    cham_cong_id = fields.Many2one('cham_cong', string="Bảng chấm công",
                                   domain="[('nhan_vien_id','=',nhan_vien_id)]")
    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng", required=True)
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)

    luong_co_ban = fields.Float("Lương cơ bản (VNĐ)", digits=(16, 0))
    he_so_cong = fields.Float("Hệ số công", default=1.0)
    phu_cap = fields.Float("Phụ cấp (VNĐ)", digits=(16, 0))
    thuong = fields.Float("Thưởng (VNĐ)", digits=(16, 0))
    khau_tru_bhxh = fields.Float("Khấu trừ BHXH (VNĐ)", digits=(16, 0))
    khau_tru_bhyt = fields.Float("Khấu trừ BHYT (VNĐ)", digits=(16, 0))
    khau_tru_khac = fields.Float("Khấu trừ khác (VNĐ)", digits=(16, 0))
    luong_thuc_linh = fields.Float(
        "Lương thực lĩnh (VNĐ)",
        compute='_compute_luong_thuc_linh',
        store=True,
        digits=(16, 0)
    )
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_duyet', 'Đã duyệt'),
        ('da_tra', 'Đã trả lương'),
    ], string="Trạng thái", default='nhap')
    display_name = fields.Char("Kỳ lương", compute='_compute_display_name', store=True)
    ghi_chu = fields.Text("Ghi chú")

    @api.depends('luong_co_ban', 'he_so_cong', 'phu_cap', 'thuong',
                 'khau_tru_bhxh', 'khau_tru_bhyt', 'khau_tru_khac')
    def _compute_luong_thuc_linh(self):
        for rec in self:
            tong_thu_nhap = rec.luong_co_ban * rec.he_so_cong + rec.phu_cap + rec.thuong
            tong_khau_tru = rec.khau_tru_bhxh + rec.khau_tru_bhyt + rec.khau_tru_khac
            rec.luong_thuc_linh = max(0, tong_thu_nhap - tong_khau_tru)

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_display_name(self):
        for rec in self:
            ten_nv = rec.nhan_vien_id.ho_ten or ''
            rec.display_name = f"Lương {ten_nv} - T{rec.thang}/{rec.nam}"

    @api.onchange('hop_dong_id')
    def _onchange_hop_dong(self):
        if self.hop_dong_id:
            self.luong_co_ban = self.hop_dong_id.luong_co_ban

    @api.onchange('cham_cong_id')
    def _onchange_cham_cong(self):
        if self.cham_cong_id:
            self.he_so_cong = self.cham_cong_id.he_so_cong

    def action_duyet(self):
        for rec in self:
            rec.trang_thai = 'da_duyet'
            
            # EVENT-DRIVEN AUTOMATION: KẾ TOÁN (TỰ ĐỘNG HẠCH TOÁN LƯƠNG)
            # Khởi tạo bút toán Tiền lương (Nợ 642 / Có 334)
            # Tìm dựa trên tk_demo đã tạo sẵn ở quan_ly_tai_chinh
            tk_chi_phi = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '642')], limit=1)
            tk_phai_tra = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '334')], limit=1)
            
            if tk_chi_phi and tk_phai_tra and rec.luong_thuc_linh > 0:
                but_toan = self.env['but_toan_ke_toan'].create({
                    'dien_giai': f'Hạch toán chi phí lương tháng {rec.thang}/{rec.nam} - {rec.nhan_vien_id.ho_ten}',
                    'tham_chieu': f'Lương {rec.nhan_vien_id.ho_ten}',
                    'nguon_goc': 'he_thong',
                    'chi_tiet_ids': [
                        (0, 0, {
                            'tai_khoan_id': tk_chi_phi.id,
                            'doi_tuong': rec.nhan_vien_id.ho_ten,
                            'dien_giai': 'Chi phí lương nhân viên',
                            'loai': 'no',
                            'so_tien': rec.luong_thuc_linh
                        }),
                        (0, 0, {
                            'tai_khoan_id': tk_phai_tra.id,
                            'doi_tuong': rec.nhan_vien_id.ho_ten,
                            'dien_giai': 'Phải trả người lao động',
                            'loai': 'co',
                            'so_tien': rec.luong_thuc_linh
                        })
                    ]
                })
                # Auto post ledger entry
                but_toan.action_ghi_so()
                
                # EVENT-DRIVEN: GỬI THÔNG BÁO TELEGRAM (FREE)
                tg_token = self.env['ir.config_parameter'].sudo().get_param('nhan_su.telegram_bot_token')
                tg_chat_id = self.env['ir.config_parameter'].sudo().get_param('nhan_su.telegram_chat_id')
                if tg_token and tg_chat_id:
                    msg = f"<b>Chào {rec.nhan_vien_id.ho_ten}</b>,\nPhiếu lương tháng {rec.thang}/{rec.nam} của bạn đã được duyệt.\nSố tiền thực lĩnh: <b>{rec.luong_thuc_linh:,.0f} VNĐ</b>."
                    from odoo.addons.nhan_su.utils.ai_messenger_utils import AIMessengerUtils
                    AIMessengerUtils.send_telegram_notification(tg_token, tg_chat_id, msg)

    def action_tra_luong(self):
        for rec in self:
            rec.trang_thai = 'da_tra'

    def action_dat_lai_nhap(self):
        for rec in self:
            rec.trang_thai = 'nhap'

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
                raise ValidationError("Đã tồn tại bảng lương cho nhân viên này trong kỳ đã chọn!")
