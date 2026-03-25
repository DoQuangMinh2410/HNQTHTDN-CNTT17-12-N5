# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class YeuCauMuaSam(models.Model):
    _name = 'yeu_cau_mua_sam'
    _description = 'Yêu cầu Mua sắm Thiết bị/Tài sản'
    _rec_name = 'ma_yeu_cau'
    _order = 'ngay_yeu_cau desc'

    ma_yeu_cau = fields.Char("Mã yêu cầu", required=True, copy=False, default='New')
    nguoi_yeu_cau_id = fields.Many2one('nhan_vien', string="Người yêu cầu", required=True)
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng ban", related='nguoi_yeu_cau_id.lich_su_cong_tac_ids.phong_ban_id')
    
    ten_thiet_bi = fields.Char("Tên thiết bị/tài sản cần mua", required=True)
    danh_muc_ts_id = fields.Many2one('danh_muc_tai_san', string="Loại tài sản dự kiến", required=True)
    so_luong = fields.Integer("Số lượng", default=1, required=True)
    don_gia_du_kien = fields.Float("Đơn giá dự kiến (VNĐ)", digits=(16, 0), required=True)
    tong_tien = fields.Float("Tổng tiền dự kiến (VNĐ)", compute='_compute_tong_tien', store=True)
    
    ly_do = fields.Text("Lý do mua sắm", required=True)
    ngay_yeu_cau = fields.Date("Ngày yêu cầu", default=fields.Date.today)
    
    tai_khoan_chi_id = fields.Many2one('tai_khoan_ke_toan', string="TK Tiền mặt/Ngân hàng (Có)", domain=[('loai_tai_khoan', '=', 'tai_san')])
    tai_khoan_ts_id = fields.Many2one('tai_khoan_ke_toan', string="TK Tài sản (Nợ)", domain=[('loai_tai_khoan', '=', 'tai_san')])

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ Trưởng phòng duyệt'),
        ('da_duyet', 'Đã duyệt & Đã mua'),
        ('tu_choi', 'Từ chối')
    ], string="Trạng thái", default='nhap', required=True)

    tai_san_sinh_ra_ids = fields.One2many('tai_san', compute='_compute_tai_san_sinh_ra', string="Tài sản đã nhập kho")

    @api.model
    def create(self, vals):
        if vals.get('ma_yeu_cau', 'New') == 'New':
            vals['ma_yeu_cau'] = 'MS-' + fields.Datetime.now().strftime('%Y%m%d%H%M%S')
        return super(YeuCauMuaSam, self).create(vals)

    @api.depends('so_luong', 'don_gia_du_kien')
    def _compute_tong_tien(self):
        for rec in self:
            rec.tong_tien = rec.so_luong * rec.don_gia_du_kien

    def _compute_tai_san_sinh_ra(self):
        # Hàm fake compute chỉ để cho đẹp form nếu cần, logic m2m sẽ tốt hơn, nhưng ta có thể tìm qua origin
        for rec in self:
            rec.tai_san_sinh_ra_ids = self.env['tai_san'].search([('ghi_chu', 'ilike', rec.ma_yeu_cau)])

    def action_gui_duyet(self):
        for rec in self:
            rec.trang_thai = 'cho_duyet'

    def action_tu_choi(self):
        for rec in self:
            rec.trang_thai = 'tu_choi'

    def action_phe_duyet_va_mua(self):
        """
        EVENT-DRIVEN: TỰ ĐỘNG KHỞI TẠO TÀI SẢN & BÚT TOÁN
        """
        for rec in self:
            if not rec.tai_khoan_chi_id or not rec.tai_khoan_ts_id:
                raise ValidationError("Để tự động sinh Bút toán, vui lòng chọn tài khoản Nợ (Tài sản) và Có (Tiền)!")
            
            # 1. Sinh Tài Sản tự động
            for i in range(rec.so_luong):
                self.env['tai_san'].create({
                    'ma_tai_san': f"TS-{rec.ma_yeu_cau}-{i+1}",
                    'ten_tai_san': rec.ten_thiet_bi,
                    'ngay_mua_ts': fields.Date.today(),
                    'gia_tri_ban_dau': rec.don_gia_du_kien,
                    'gia_tri_hien_tai': rec.don_gia_du_kien,
                    'danh_muc_ts_id': rec.danh_muc_ts_id.id,
                    'ghi_chu': f"Tự động tạo từ Yêu cầu mua sắm: {rec.ma_yeu_cau}",
                    'pp_khau_hao': 'straight-line',
                    'thoi_gian_toi_da': 5
                })

            # 2. Sinh Bút toán Kế toán tự động
            but_toan = self.env['but_toan_ke_toan'].create({
                'dien_giai': f"Hạch toán mua sắm tài sản theo {rec.ma_yeu_cau}",
                'tham_chieu': rec.ma_yeu_cau,
                'nguon_goc': 'he_thong',
                'chi_tiet_ids': [
                    (0, 0, {
                        'tai_khoan_id': rec.tai_khoan_ts_id.id,
                        'doi_tuong': rec.nguoi_yeu_cau_id.ho_ten,
                        'dien_giai': f"Tăng tài sản cố định: {rec.ten_thiet_bi}",
                        'loai': 'no',
                        'so_tien': rec.tong_tien
                    }),
                    (0, 0, {
                        'tai_khoan_id': rec.tai_khoan_chi_id.id,
                        'doi_tuong': rec.nguoi_yeu_cau_id.ho_ten,
                        'dien_giai': f"Thanh toán tiền mua tài sản",
                        'loai': 'co',
                        'so_tien': rec.tong_tien
                    })
                ]
            })
            # Tự động ghi sổ
            but_toan.action_ghi_so()

            # EVENT-DRIVEN: GỬI THÔNG BÁO TELEGRAM (FREE)
            tg_token = self.env['ir.config_parameter'].sudo().get_param('nhan_su.telegram_bot_token')
            tg_chat_id = self.env['ir.config_parameter'].sudo().get_param('nhan_su.telegram_chat_id')
            if tg_token and tg_chat_id:
                msg = f"<b>Thông báo mua sắm</b>\nYêu cầu {rec.ma_yeu_cau} (<i>{rec.ten_thiet_bi}</i>) đã được phê duyệt và khởi tạo tài sản thành công."
                from odoo.addons.nhan_su.utils.ai_messenger_utils import AIMessengerUtils
                AIMessengerUtils.send_telegram_notification(tg_token, tg_chat_id, msg)

            rec.trang_thai = 'da_duyet'

    @api.model
    def create(self, vals):
        if vals.get('ma_yeu_cau', 'New') == 'New':
            vals['ma_yeu_cau'] = self.env['ir.sequence'].next_by_code('yeu.cau.mua.sam.seq') or 'New'
        return super(YeuCauMuaSam, self).create(vals)
