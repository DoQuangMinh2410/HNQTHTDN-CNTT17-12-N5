# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    
    telegram_bot_token = fields.Char(
        string="Telegram Bot Token",
        config_parameter='nhan_su.telegram_bot_token',
        help="Token nhận từ @BotFather."
    )
    
    telegram_chat_id = fields.Char(
        string="Telegram Chat ID (Mặc định)",
        config_parameter='nhan_su.telegram_chat_id',
        help="ID người nhận hoặc Group ID nhận thông báo."
    )

    def action_test_telegram_connection(self):
        """
        Kiểm tra kết nối tới Telegram Bot.
        """
        self.ensure_one()
        token = self.telegram_bot_token or self.env['ir.config_parameter'].sudo().get_param('nhan_su.telegram_bot_token')
        chat_id = self.telegram_chat_id or self.env['ir.config_parameter'].sudo().get_param('nhan_su.telegram_chat_id')
        
        if not token or not chat_id:
            raise models.ValidationError("Vui lòng nhập đầy đủ Token và Chat ID trước khi kiểm tra!")
        
        from odoo.addons.hndn_ai_base.utils.ai_messenger_utils import AIMessengerUtils
        success, res_msg = AIMessengerUtils.send_telegram_notification(
            token.strip(), 
            chat_id.strip(), 
            "<b>Thông báo từ Odoo</b>\nKết nối Telegram thành công! ✅"
        )
        
        if success:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Thành công',
                    'message': 'Đã gửi tin nhắn kiểm tra tới Telegram!',
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            raise models.ValidationError(f"Gửi tin nhắn thất bại! Chi tiết lỗi: {res_msg}")
