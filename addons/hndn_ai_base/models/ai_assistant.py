# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AIAssistant(models.Model):
    _name = 'ai_assistant'
    _description = 'HNDN AI Virtual Assistant'
    _rec_name = 'question'
    _order = 'create_date desc'

    question = fields.Text("Câu hỏi cuối", readonly=True)
    answer = fields.Text("Trả lời cuối", readonly=True)
    user_id = fields.Many2one('res.users', string="Người hỏi", default=lambda self: self.env.user, readonly=True)
    message_ids = fields.One2many('ai_chat_message', 'session_id', string="Lịch sử hội thoại")
    suggested_questions = fields.Text("Câu hỏi gợi ý (JSON)", help="Lưu danh sách câu hỏi gợi ý dạng JSON")

    def action_ask_ai(self):
        for rec in self:
            api_key = self.env['ir.config_parameter'].sudo().get_param('hndn_ai_base.hndn_gemini_api_key')
            if not api_key:
                return "Vui lòng cấu hình Gemini API Key!"

            # 1. Lấy lịch sử 10 tin nhắn gần nhất
            history = ""
            messages = self.env['ai_chat_message'].search([('session_id', '=', rec.id)], order='create_date desc', limit=10)
            for msg in reversed(messages):
                history += f"{'User' if msg.role == 'user' else 'AI'}: {msg.content}\n"

            # 2. Lấy câu hỏi mới nhất (thường là cái vừa được create/write vào message_ids)
            last_user_msg = self.env['ai_chat_message'].search([('session_id', '=', rec.id), ('role', '=', 'user')], order='create_date desc', limit=1)
            if not last_user_msg:
                 continue
            
            question = last_user_msg.content
            
            # 3. Thu thập ngữ cảnh bổ sung dựa trên từ khóa
            extra_context = ""
            if any(k in question.lower() for k in ['tài sản', 'mượn', 'trả', 'bảo hành']):
                assets = self.env['tai_san'].search([], limit=5)
                asset_info = "\n".join([f"- {a.ten_tai_san} ({a.ma_tai_san}): Bảo hành tới {a.ngay_het_han_bao_hanh or 'N/A'}" for a in assets])
                extra_context += f"\nThông tin một số tài sản:\n{asset_info}\n"
            
            if any(k in question.lower() for k in ['nhân viên', 'lương', 'phòng ban']):
                employees = self.env['nhan_vien'].search([], limit=5)
                emp_info = "\n".join([f"- {e.ten_nv}: {e.phong_ban_id.ten_phong_ban or 'N/A'}" for e in employees])
                extra_context += f"\nThông tin nhân sự:\n{emp_info}\n"

            system_prompt = f"""Bạn là trợ lý ảo của công ty HNDN. 
Hãy trả lời các thắc mắc của nhân viên một cách lịch sự, chuyên nghiệp.
{extra_context}
Dựa trên lịch sử hội thoại sau:
{history}
"""
            
            from odoo.addons.hndn_ai_base.utils.ai_messenger_utils import AIMessengerUtils
            response = AIMessengerUtils.get_gemini_response(api_key, f"{system_prompt}\nCâu hỏi hiện tại: {question}")
            
            if response:
                # Lưu câu trả lời vào history
                self.env['ai_chat_message'].create({
                    'session_id': rec.id,
                    'role': 'assistant',
                    'content': response
                })
                rec.answer = response # Cập nhật answer cuối để tương thích giao diện cũ
                
                # Tạo gợi ý câu hỏi liên quan dựa trên context
                suggestions = [
                    "Hướng dẫn quy trình mượn tài sản",
                    "Kiểm tra lịch trống của tài sản",
                    "Tra cứu thông tin bảo hành",
                    "Giải thích các quy định công ty"
                ]
                import json
                rec.suggested_questions = json.dumps(suggestions)
            else:
                rec.answer = "Đã có lỗi xảy ra khi kết nối với AI."

    def get_conversation_data(self):
        self.ensure_one()
        messages = [{
            'id': m.id,
            'role': m.role,
            'content': m.content,
            'create_date': m.create_date,
        } for m in self.message_ids]
        
        import json
        suggestions = []
        if self.suggested_questions:
            try:
                suggestions = json.loads(self.suggested_questions)
            except:
                pass
                
        return {
            'messages': messages,
            'suggestions': suggestions
        }

class AIChatMessage(models.Model):
    _name = 'ai_chat_message'
    _description = 'Lịch sử tin nhắn AI'
    _order = 'create_date asc'

    session_id = fields.Many2one('ai_assistant', string="Phiên chat", ondelete='cascade')
    role = fields.Selection([('user', 'User'), ('assistant', 'AI')], string="Vai trò")
    content = fields.Text("Nội dung")
