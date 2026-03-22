# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AssetGeminiConfig(models.Model):
    """Cấu hình Google Gemini API"""
    _name = 'asset.gemini.config'
    _description = 'Cấu hình Google Gemini AI'
    _rec_name = 'name'

    name = fields.Char('Tên cấu hình', required=True, default='Gemini Configuration')
    
    # API Configuration
    gemini_api_key = fields.Char(
        'API Key Google Gemini',
        required=True,
        help='Lấy từ: https://aistudio.google.com/app/apikeys'
    )
    
    model_name = fields.Selection([
        ('gemini-1.5-pro', 'Gemini 1.5 Pro (Recommended)'),
        ('gemini-1.5-flash', 'Gemini 1.5 Flash (Fast)'),
        ('gemini-pro', 'Gemini Pro'),
    ], string='Model', default='gemini-1.5-pro', required=True)
    
    # Temperature for creativity (0.0 = deterministic, 1.0 = creative)
    temperature = fields.Float(
        'Temperature',
        default=0.7,
        help='0.0 = Deterministic (phù hợp báo cáo), 1.0 = Creative'
    )
    
    max_tokens = fields.Integer(
        'Max Output Tokens',
        default=2000,
        help='Độ dài tối đa của câu trả lời'
    )
    
    language = fields.Selection([
        ('vi', 'Tiếng Việt (Recommended)'),
        ('en', 'English'),
        ('auto', 'Auto-detect'),
    ], string='Ngôn ngữ phân tích', default='vi')
    
    # Status
    is_active = fields.Boolean('Kích hoạt', default=True)
    is_configured = fields.Boolean('Đã cấu hình', compute='_compute_is_configured', store=True)
    
    # Test connection
    last_test = fields.Datetime('Lần test cuối')
    test_status = fields.Selection([
        ('success', 'Thành công'),
        ('failed', 'Thất bại'),
        ('not_tested', 'Chưa test'),
    ], string='Trạng thái test', default='not_tested')
    test_message = fields.Text('Tin nhắn test')

    @api.depends('gemini_api_key')
    def _compute_is_configured(self):
        for record in self:
            record.is_configured = bool(record.gemini_api_key)

    def action_test_connection(self):
        """Test kết nối tới Gemini API"""
        try:
            import google.generativeai as genai
            
            # Test API key
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel(self.model_name)
            
            # Send simple test message
            response = model.generate_content(
                "Xin chào! Đây là test connection. Hãy trả lời bằng 1 câu ngắn.",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=100,
                    temperature=0.7,
                )
            )
            
            if response.text:
                self.last_test = fields.Datetime.now()
                self.test_status = 'success'
                self.test_message = f"✅ Connection successful!\n\nResponse: {response.text[:200]}"
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Thành công',
                        'message': 'Kết nối Gemini API thành công!',
                        'type': 'success',
                        'sticky': True,
                    }
                }
        except ImportError:
            self.test_status = 'failed'
            self.test_message = "❌ Error: google-generativeai module not installed.\nRun: pip install google-generativeai"
            raise ValidationError("Cần cài đặt: pip install google-generativeai")
        except Exception as e:
            self.last_test = fields.Datetime.now()
            self.test_status = 'failed'
            self.test_message = f"❌ Connection failed: {str(e)}"
            raise ValidationError(f"Lỗi kết nối Gemini: {str(e)}")

    def get_active_config(self):
        """Lấy cấu hình Gemini đang hoạt động"""
        config = self.search([('is_active', '=', True)], limit=1)
        if not config:
            raise ValidationError("Vui lòng cấu hình Gemini API key trước.")
        return config
