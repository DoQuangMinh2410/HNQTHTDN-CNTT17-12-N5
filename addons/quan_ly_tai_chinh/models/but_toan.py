from odoo import models, fields, api
from odoo.exceptions import ValidationError
# from odoo.addons.nhan_su.utils.ai_messenger_utils import AIMessengerUtils
import json


class ButToan(models.Model):
    _name = 'but_toan_ke_toan'
    _description = 'Bút toán Sổ cái (Journal Entry)'
    _rec_name = 'so_chung_tu'
    _order = 'ngay_ghi_so desc'

    so_chung_tu = fields.Char("Số chứng từ", required=True, copy=False, default='New')
    ngay_ghi_so = fields.Date("Ngày ghi sổ", required=True, default=fields.Date.today)
    dien_giai = fields.Char("Diễn giải", required=True)
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_ghi_so', 'Đã ghi sổ'),
    ], string="Trạng thái", default='nhap', required=True)
    
    invoice_file = fields.Binary("File Hóa đơn (AI OCR)", attachment=True)

    def action_ai_ocr_invoice(self):
        for rec in self:
            if not rec.invoice_file:
                raise ValidationError("Vui lòng tải lên ảnh hóa đơn trước khi thực hiện bóc tách AI!")
            
            try:
                from odoo.addons.hndn_ai_base.utils.ai_messenger_utils import AIMessengerUtils
            except ImportError:
                raise ValidationError("Không tìm thấy công cụ AI trong module Nhân sự!")

            api_key = self.env['ir.config_parameter'].sudo().get_param('hndn_ai_base.hndn_gemini_api_key')
            if not api_key:
                raise ValidationError("Chưa cấu hình Gemini API Key! Vui lòng vào Thiết lập Nhân sự để cấu hình.")

            prompt = """
            Hãy phân tích hóa đơn này và trả về kết quả dưới dạng JSON với các trường:
            ngay_ghi_so (YYYY-MM-DD), dien_giai, tong_tien, nha_cung_cap.
            Chỉ trả về JSON, không giải thích thêm.
            """
            
            response_text = AIMessengerUtils.get_gemini_response(api_key, prompt, image_data=rec.invoice_file)
            if response_text:
                try:
                    # Làm sạch JSON
                    clean_json = response_text
                    if '```json' in response_text:
                        clean_json = response_text.split('```json')[1].split('```')[0].strip()
                    elif '```' in response_text:
                        clean_json = response_text.split('```')[1].split('```')[0].strip()
                    
                    data = json.loads(clean_json)
                    
                    rec.write({
                        'ngay_ghi_so': data.get('ngay_ghi_so'),
                        'dien_giai': data.get('dien_giai') or f"Hóa đơn từ {data.get('nha_cung_cap')}",
                    })
                except Exception as e:
                    raise ValidationError(f"Lỗi khi xử lý dữ liệu từ AI: {str(e)}")
            else:
                raise ValidationError("AI không phản hồi hoặc gặp lỗi kết nối.")
    
    chi_tiet_ids = fields.One2many('chi_tiet_but_toan', 'but_toan_id', string="Chi tiết Nợ/Có")
    tong_no = fields.Float("Tổng Nợ", compute='_compute_tong', store=True, digits=(16, 0))
    tong_co = fields.Float("Tổng Có", compute='_compute_tong', store=True, digits=(16, 0))

    # Liên kết ngoại (để truy vết)
    tham_chieu = fields.Char("Tham chiếu (Hợp đồng/Lương/Tài sản)")
    nguon_goc = fields.Selection([
        ('thu_cong', 'Bút toán thủ công'),
        ('he_thong', 'Bút toán tự động (System)'),
    ], string="Nguồn gốc", default='thu_cong')


    @api.depends('chi_tiet_ids.so_tien', 'chi_tiet_ids.loai')
    def _compute_tong(self):
        for rec in self:
            rec.tong_no = sum(rec.chi_tiet_ids.filtered(lambda x: x.loai == 'no').mapped('so_tien'))
            rec.tong_co = sum(rec.chi_tiet_ids.filtered(lambda x: x.loai == 'co').mapped('so_tien'))

    def action_ghi_so(self):
        for rec in self:
            if not rec.chi_tiet_ids:
                raise ValidationError("Bút toán phải có ít nhất 1 dòng chi tiết!")
            if abs(rec.tong_no - rec.tong_co) > 0.01:
                raise ValidationError(f"Tổng Nợ ({rec.tong_no}) và Có ({rec.tong_co}) phải cân bằng!")
            rec.trang_thai = 'da_ghi_so'

    def action_huy_ghi_so(self):
        for rec in self:
            rec.trang_thai = 'nhap'

    @api.model
    def create(self, vals):
        if vals.get('so_chung_tu', 'New') == 'New':
            vals['so_chung_tu'] = self.env['ir.sequence'].next_by_code('but.toan.seq') or 'New'
        return super(ButToan, self).create(vals)
