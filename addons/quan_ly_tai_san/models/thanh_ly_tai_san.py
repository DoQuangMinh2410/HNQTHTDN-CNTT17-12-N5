from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class ThanhLyTaiSan(models.Model):
    _name = 'thanh_ly_tai_san'
    _description = 'Bảng chứa thông tin Thanh lý tài sản'
    _rec_name = 'ma_thanh_ly'
    _sql_constraints = [
        ("ma_thanh_ly_unique", "unique(ma_thanh_ly)", "Mã thanh lý đã tồn tại"),
    ]

    ma_thanh_ly = fields.Char('Mã thanh lý', required=True, default='New', copy=False)
    hanh_dong = fields.Selection([
        ('ban', 'Bán'),
        ('huy', 'Tiêu hủy')
    ], string='Hành động', required=True)
    tai_san_id = fields.Many2one('tai_san', 'Tài sản', required=True, ondelete='cascade')
    nguoi_thanh_ly_id = fields.Many2one('nhan_vien', 'Người thực hiện', required=True)
    thoi_gian_thanh_ly = fields.Datetime('Thời gian thanh lý', required=True, default=fields.Datetime.now)
    ly_do_thanh_ly = fields.Char('Lý do thanh lý', default='')
    gia_ban = fields.Float('Giá bán', required=True)
    gia_goc = fields.Float('Giá gốc', compute='_compute_gia_goc', store=True)

    trang_thai = fields.Selection([
        ('nhap', 'Mới lập'),
        ('da_duyet', 'Đã duyệt thanh lý'),
    ], string='Trạng thái', default='nhap', required=True)

    def action_duyet(self):
        for rec in self:
            # EVENT-DRIVEN AUTOMATION: KẾ TOÁN (GHI NHẬN THU NHẬP THANH LÝ)
            # Nợ 1111 (Tiền mặt) / Có 711 (Thu nhập khác)
            tk_tien_mat = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '1111')], limit=1)
            tk_thu_nhap = self.env['tai_khoan_ke_toan'].search([('ma_tai_khoan', '=', '711')], limit=1)

            if tk_tien_mat and tk_thu_nhap and rec.gia_ban > 0:
                but_toan = self.env['but_toan_ke_toan'].create({
                    'dien_giai': f"Thu nhập thanh lý tài sản {rec.tai_san_id.ten_tai_san} - {rec.ma_thanh_ly}",
                    'tham_chieu': rec.ma_thanh_ly,
                    'nguon_goc': 'he_thong',
                    'chi_tiet_ids': [
                        (0, 0, {
                            'tai_khoan_id': tk_tien_mat.id,
                            'dien_giai': f"Thu tiền thanh lý {rec.tai_san_id.ten_tai_san}",
                            'loai': 'no',
                            'so_tien': rec.gia_ban
                        }),
                        (0, 0, {
                            'tai_khoan_id': tk_thu_nhap.id,
                            'dien_giai': f"Hạch toán thu nhập thanh lý TSCĐ",
                            'loai': 'co',
                            'so_tien': rec.gia_ban
                        })
                    ]
                })
                but_toan.action_ghi_so()

            rec.trang_thai = 'da_duyet'
                                         
    @api.constrains('gia_ban')
    def _constrains_gia_ban(self):
        for record in self:
            if record.gia_ban < 0:
                raise ValidationError("Giá bán không thể nhỏ hơn 0")
    
    @api.depends('tai_san_id')
    def _compute_gia_goc(self):
        for record in self:
            if record.tai_san_id:
                record.gia_goc = record.tai_san_id.gia_tri_ban_dau
                
    @api.constrains('tai_san_id')
    def _check_tai_san_thanh_ly_once(self):
        for record in self:
            existing_thanh_ly = self.env['thanh_ly_tai_san'].search([
                ('tai_san_id', '=', record.tai_san_id.id),
                ('id', '!=', record.id)
            ])
            if existing_thanh_ly:
                raise ValidationError(_(f"Tài sản '{record.tai_san_id.ten_tai_san}' đã được thanh lý trước đó!"))

    @api.model
    def create(self, vals):
        if vals.get('ma_thanh_ly', 'New') == 'New':
            vals['ma_thanh_ly'] = self.env['ir.sequence'].next_by_code('thanh.ly.seq') or 'New'
        return super(ThanhLyTaiSan, self).create(vals)
