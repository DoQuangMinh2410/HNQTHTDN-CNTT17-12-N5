from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.addons.hndn_ai_base.utils.ai_messenger_utils import AIMessengerUtils
import json


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'

    # ---- Thông tin cơ bản ----
    ma_dinh_danh = fields.Char("Mã định danh", required=True, copy=False, default='New')
    anh_dai_dien = fields.Binary("Ảnh đại diện", attachment=True)
    ho_ten = fields.Char("Họ tên", required=True, default='')
    ngay_sinh = fields.Date("Ngày sinh")
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác'),
    ], string="Giới tính", default='nam')
    tinh_trang_hon_nhan = fields.Selection([
        ('doc_than', 'Độc thân'),
        ('da_ket_hon', 'Đã kết hôn'),
        ('ly_hon', 'Ly hôn'),
    ], string="Tình trạng hôn nhân", default='doc_than')

    # ---- Liên hệ ----
    so_cccd = fields.Char("Số CCCD/CMND")
    ngay_cap_cccd = fields.Date("Ngày cấp")
    noi_cap_cccd = fields.Char("Nơi cấp")
    que_quan = fields.Char("Quê quán")
    dia_chi_thuong_tru = fields.Char("Địa chỉ thường trú")
    dia_chi_tam_tru = fields.Char("Địa chỉ tạm trú")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")

    cv_file = fields.Binary("File CV (PDF/Ảnh)", attachment=True)
    
    trang_thai = fields.Selection([
        ('dang_lam', 'Đang làm việc'),
        ('nghi_viec', 'Đã nghỉ việc')
    ], string="Trạng thái", default='dang_lam', required=True)

    def action_ai_ocr_cv(self):
        for rec in self:
            if not rec.cv_file:
                raise ValidationError("Vui lòng tải lên file CV trước khi thực hiện bóc tách AI!")
            
            api_key = self.env['ir.config_parameter'].sudo().get_param('hndn_ai_base.hndn_gemini_api_key')
            if not api_key:
                raise ValidationError("Chưa cấu hình Gemini API Key!")

            prompt = """
            Hãy phân tích CV này và trả về kết quả dưới dạng JSON với các trường:
            ho_ten, ngay_sinh (YYYY-MM-DD), gioi_tinh (nam/nu/khac), email, so_dien_thoai, trinh_do_hoc_van (thpt/trung_cap/cao_dang/dai_hoc/thac_si/tien_si), chuyen_nganh, truong_dao_tao.
            Chỉ trả về JSON, không giải thích thêm.
            """
            
            response_text = AIMessengerUtils.get_gemini_response(api_key, prompt, image_data=rec.cv_file)
            if response_text:
                try:
                    # Làm sạch chuỗi JSON nếu Gemini trả về markdown code block
                    clean_json = response_text.replace('```json', '').replace('```', '').strip()
                    data = json.loads(clean_json)
                    
                    rec.write({
                        'ho_ten': data.get('ho_ten', rec.ho_ten),
                        'ngay_sinh': data.get('ngay_sinh'),
                        'gioi_tinh': data.get('gioi_tinh', 'nam'),
                        'email': data.get('email', rec.email),
                        'so_dien_thoai': data.get('so_dien_thoai', rec.so_dien_thoai),
                        'trinh_do_hoc_van': data.get('trinh_do_hoc_van'),
                        'chuyen_nganh': data.get('chuyen_nganh'),
                        'truong_dao_tao': data.get('truong_dao_tao'),
                    })
                except Exception as e:
                    raise ValidationError(f"Lỗi khi xử lý dữ liệu từ AI: {str(e)}")
            else:
                raise ValidationError("AI không phản hồi hoặc gặp lỗi kết nối.")

    @api.constrains('trang_thai')
    def _check_asset_return_on_resignation(self):
        for rec in self:
            if rec.trang_thai == 'nghi_viec':
                # Kiểm tra xem nhân viên có đang mượn tài sản nào không
                muon_tai_san = self.env['muon_tra_tai_san'].search([
                    ('nhan_vien_muon_id', '=', rec.id),
                    ('trang_thai', '=', 'dang-muon')
                ])
                if muon_tai_san:
                    raise ValidationError(f"Nhân viên {rec.ho_ten} vẫn còn tài sản đang mượn chưa trả. Vui lòng kiểm tra lại trước khi cho nghỉ việc!")

    # ---- Học vấn & Chuyên môn ----
    trinh_do_hoc_van = fields.Selection([
        ('thpt', 'THPT'),
        ('trung_cap', 'Trung cấp'),
        ('cao_dang', 'Cao đẳng'),
        ('dai_hoc', 'Đại học'),
        ('thac_si', 'Thạc sĩ'),
        ('tien_si', 'Tiến sĩ'),
    ], string="Trình độ học vấn")
    chuyen_nganh = fields.Char("Chuyên ngành")
    truong_dao_tao = fields.Char("Trường đào tạo")

    # ---- Ngân hàng ----
    so_tai_khoan_ngan_hang = fields.Char("Số tài khoản ngân hàng")
    ten_ngan_hang = fields.Char("Tên ngân hàng")
    chi_nhanh_ngan_hang = fields.Char("Chi nhánh")

    # ---- Quan hệ ----
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac",
        inverse_name="nhan_vien_id",
        string="Lịch sử công tác"
    )
    hop_dong_ids = fields.One2many(
        "hop_dong",
        inverse_name="nhan_vien_id",
        string="Hợp đồng lao động"
    )
    cham_cong_ids = fields.One2many(
        "cham_cong",
        inverse_name="nhan_vien_id",
        string="Chấm công"
    )
    tinh_luong_ids = fields.One2many(
        "tinh_luong",
        inverse_name="nhan_vien_id",
        string="Bảng lương"
    )
    phep_nam_ids = fields.One2many(
        "phep_nam",
        inverse_name="nhan_vien_id",
        string="Đơn nghỉ phép"
    )
    khen_thuong_ky_luat_ids = fields.One2many(
        "khen_thuong_ky_luat",
        inverse_name="nhan_vien_id",
        string="Khen thưởng - Kỷ luật"
    )

    @api.depends('ngay_sinh')
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                record.tuoi = (fields.Date.today() - record.ngay_sinh).days // 365
            else:
                record.tuoi = 0

    @api.model
    def create(self, vals):
        if vals.get('ma_dinh_danh', 'New') == 'New':
            vals['ma_dinh_danh'] = self.env['ir.sequence'].next_by_code('nhan.vien.seq') or 'New'
        return super(NhanVien, self).create(vals)
