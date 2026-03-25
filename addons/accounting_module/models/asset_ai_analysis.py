# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import json
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class AssetAIAnalysis(models.Model):
    _name = 'asset.ai.analysis'
    _description = 'Phân tích AI tài sản'
    _rec_name = 'analysis_date'

    analysis_date = fields.Date('Ngày phân tích', default=fields.Date.today)
    
    # Dữ liệu phân tích
    total_assets = fields.Integer('Tổng số tài sản')
    total_value = fields.Float('Tổng giá trị')
    average_depreciation = fields.Float('Khấu hao trung bình hàng tháng')
    
    # Recommendation
    analysis_text = fields.Text('Kết quả phân tích')
    recommendations = fields.Text('Khuyến nghị')
    
    anomalies = fields.Text('Các điểm bất thường')
    
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('analyzed', 'Đã phân tích'),
    ], string='Trạng thái', default='draft')

    def action_analyze(self):
        """Thực hiện phân tích AI"""
        # Lấy dữ liệu
        assets = self.env['tai_san'].search([('pp_khau_hao', '!=', 'none')])
        
        self.total_assets = len(assets)
        self.total_value = sum(asset.gia_tri_ban_dau for asset in assets)
        
        # Tính khấu hao trung bình
        depreciation_records = self.env['asset.depreciation'].search([])
        if depreciation_records:
            self.average_depreciation = sum(d.depreciation_amount for d in depreciation_records) / len(depreciation_records)
        
        # Phân tích đơn giản (không dùng API bên ngoài lần này)
        analysis = self._perform_local_analysis(assets)
        
        self.analysis_text = analysis['analysis']
        self.recommendations = analysis['recommendations']
        self.anomalies = analysis['anomalies']
        
        self.state = 'analyzed'
        
        # Gửi thông báo nếu phát hiện bất thường
        self._send_anomaly_notification(analysis)

    def _perform_local_analysis(self, assets):
        """Phân tích dữ liệu bằng Google Gemini AI"""
        # Phân loại theo trạng thái
        in_use_assets = assets.filtered(lambda a: hasattr(a, 'usage_status') and a.usage_status == 'in_use')
        broken_assets = assets.filtered(lambda a: hasattr(a, 'usage_status') and a.usage_status == 'broken')
        
        # Chuẩn bị dữ liệu cho Gemini
        data_summary = f"""
Tóm tắt dữ liệu Tài sản (ngày {datetime.now().strftime('%d/%m/%Y')}):
- Tổng số tài sản: {self.total_assets}
- Tổng giá trị: {self.total_value:,.0f} VNĐ
- Khấu hao trung bình hàng tháng: {self.average_depreciation:,.0f} VNĐ
- Tài sản đang sử dụng: {len(in_use_assets)}
- Tài sản hư hỏng: {len(broken_assets)}

Chi tiết tài sản:
"""
        for asset in assets[:10]:  # Top 10 tài sản
            data_summary += f"- {asset.ten_tai_san}: {asset.gia_tri_ban_dau:,.0f} VNĐ (Trạng thái: {getattr(asset, 'usage_status', 'N/A')})\n"
        
        try:
            # Thử dùng Gemini nếu được cấu hình
            analysis_result = self._analyze_with_gemini(data_summary)
            if analysis_result:
                return analysis_result
        except Exception as e:
            _logger.warning(f"Gemini analysis failed: {str(e)}. Falling back to local analysis.")
        
        # Fallback: Local analysis nếu Gemini không khả dụng
        return self._perform_fallback_analysis(assets, in_use_assets, broken_assets)

    def _analyze_with_gemini(self, data_summary):
        """Gọi Google Gemini API để phân tích"""
        try:
            import google.generativeai as genai
        except ImportError:
            _logger.warning("google-generativeai not installed. Skipping Gemini analysis.")
            return None
        
        try:
            # Lấy cấu hình Gemini
            config_model = self.env['asset.gemini.config']
            gemini_config = config_model.get_active_config()
            
            # Configure Gemini
            genai.configure(api_key=gemini_config.gemini_api_key)
            model = genai.GenerativeModel(gemini_config.model_name)
            
            # Prompt cho phân tích tài sản
            prompt = f"""
Bạn là một chuyên gia tài chính / quản lý tài sản. Hãy phân tích dữ liệu tài sản sau và cung cấp:
1. Phân tích chi tiết (Analysis)
2. Khuyến nghị tối ưu hóa (Recommendations)
3. Các điểm bất thường cần chú ý (Anomalies)

Dữ liệu:
{data_summary}

Yêu cầu:
- Trả lời bằng Tiếng Việt
- Cấu trúc rõ ràng với emojis
- Đưa ra các khuyến nghị cụ thể và thực tế
- Nhấn mạnh các rủi ro tài chính

Format trả lời:
📊 PHÂN TÍCH TÀI SẢN
[Nội dung phân tích]

💡 KHUYẾN NGHỊ
[Danh sách khuyến nghị]

⚠️ ĐIỂM BẤT THƯỜNG
[Danh sách điểm cần lưu ý]
"""
            
            # Gọi Gemini API
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=gemini_config.max_tokens,
                    temperature=gemini_config.temperature,
                )
            )
            
            if response.text:
                # Parse response
                result = self._parse_gemini_response(response.text)
                _logger.info("Gemini analysis completed successfully")
                return result
        
        except Exception as e:
            _logger.error(f"Gemini API error: {str(e)}")
            return None

    def _parse_gemini_response(self, response_text):
        """Parse phản hồi từ Gemini"""
        # Split response theo sections
        analysis_text = ""
        recommendations = ""
        anomalies = ""
        
        sections = response_text.split('\n\n')
        for section in sections:
            if '📊' in section or 'PHÂN TÍCH' in section:
                analysis_text = section
            elif '💡' in section or 'KHUYẾN NGHỊ' in section:
                recommendations = section
            elif '⚠️' in section or 'BẤT THƯỜNG' in section:
                anomalies = section
        
        return {
            'analysis': analysis_text or "📊 Phân tích AI từ Gemini\n" + response_text[:500],
            'recommendations': recommendations or "💡 Khuyến nghị từ AI",
            'anomalies': anomalies or "⚠️ Không phát hiện bất thường"
        }

    def _perform_fallback_analysis(self, assets, in_use_assets, broken_assets):
        """Phân tích fallback (cục bộ) khi Gemini không khả dụng"""
        analysis_text = "📊 PHÂN TÍCH TÀI SẢN (Local Analysis)\n"
        analysis_text += f"Ngày phân tích: {datetime.now().strftime('%d/%m/%Y')}\n\n"
        
        analysis_text += f"📈 Tổng Thông Số:\n"
        analysis_text += f"  • Tổng số tài sản: {self.total_assets}\n"
        analysis_text += f"  • Tổng giá trị: {self.total_value:,.0f} VNĐ\n"
        analysis_text += f"  • Khấu hao trung bình/tháng: {self.average_depreciation:,.0f} VNĐ\n\n"
        
        analysis_text += f"📦 Phân Loại Tài Sản:\n"
        analysis_text += f"  • Đang sử dụng: {len(in_use_assets)}\n"
        analysis_text += f"  • Hư hỏng: {len(broken_assets)}\n\n"
        
        recommendations = "💡 KHUYẾN NGHỊ:\n"
        
        # Khuyến nghị 1: Tối ưu khấu hao
        if self.total_value > 1000000000:  # > 1 tỷ
            recommendations += "  • Xem xét tăng thời gian khấu hao để giảm chi phí hàng tháng\n"
        
        if len(broken_assets) > len(in_use_assets) * 0.2:
            recommendations += "  • Số lượng tài sản hư hỏng cao. Cân nhắc nâng cấp hệ thống bảo trì\n"
        
        recommendations += "  • Định kỳ kiểm tra tài sản hàng quý\n"
        recommendations += "  • Cập nhật giá trị tài sản khi có điều chỉnh giá\n\n"
        
        # Phát hiện bất thường
        anomalies = "⚠️ ĐIỂM BẤT THƯỜNG:\n"
        has_anomalies = False
        
        for asset in assets:
            if hasattr(asset, 'gia_tri_hien_tai') and asset.gia_tri_hien_tai <= asset.gia_tri_ban_dau * 0.1:
                anomalies += f"  • Tài sản '{asset.ten_tai_san}' đã khấu hao > 90%\n"
                has_anomalies = True
        
        if not has_anomalies:
            anomalies += "  • Không phát hiện bất thường\n"
        
        return {
            'analysis': analysis_text,
            'recommendations': recommendations,
            'anomalies': anomalies,
        }

    def _send_anomaly_notification(self, analysis):
        """Gửi thông báo khi phát hiện bất thường"""
        try:
            # Kiểm tra xem có phát hiện bất thường không
            anomalies_text = analysis.get('anomalies', '')
            if '• Không phát hiện bất thường' in anomalies_text:
                return  # Không có bất thường, bỏ qua

            # Kiểm tra cấu hình thông báo
            email_configs = self.env['notify.email.config'].search([('is_active', '=', True)])
            sms_configs = self.env['notify.sms.config'].search([('is_active', '=', True)])
            
            if not (email_configs or sms_configs):
                return  # Không cấu hình thông báo
            
            # Chuẩn bị nội dung thông báo
            notification_type = 'email_sms' if (email_configs and sms_configs) else ('email' if email_configs else 'sms')
            
            email_body = f"""
Phân tích AI phát hiện bất thường trong dữ liệu tài sản

Ngày phân tích: {self.analysis_date.strftime('%d/%m/%Y')}

{analysis.get('anomalies', 'Không phát hiện')}

Khuyến nghị:
{analysis.get('recommendations', '')}

Vui lòng truy cập hệ thống để xem chi tiết phân tích đầy đủ.
"""
            
            sms_message = "⚠️ Phát hiện bất thường trong tài sản. Vui lòng kiểm tra hệ thống ngay."[:160]
            
            # Lấy danh sách nhận thông báo
            recipients = self._get_notification_recipients()
            
            for recipient in recipients:
                notification_log = self.env['notification.log'].create_log(
                    subject=f'🚨 Phát hiện bất thường trong Tài sản',
                    event_type='anomaly_detected',
                    notification_type=notification_type,
                    email_to=recipient.get('email'),
                    sms_to=recipient.get('phone'),
                    subject_line=f'Cảnh báo bất thường - {self.analysis_date.strftime("%d/%m/%Y")}',
                    email_body_text=email_body,
                    sms_message=sms_message,
                    analysis_id=self.id,
                    email_provider=email_configs[0].email_provider if email_configs else None,
                    sms_provider=sms_configs[0].sms_provider if sms_configs else None,
                )
                
                # Gửi thông báo
                self.env['notification.service'].send_notification(notification_log)
                _logger.info(f'Anomaly alert sent to {recipient.get("email")}')
                
        except Exception as e:
            _logger.error(f'Error sending anomaly notification: {str(e)}')
            # Không throw error để không ảnh hưởng đến phân tích

    def _get_notification_recipients(self):
        """Lấy danh sách nhận thông báo"""
        recipients = []
        
        # Lấy từ danh sách system users
        config_users = self.env['res.users'].search([('groups_id', '=', self.env.ref('base.group_system').id)])
        for user in config_users[:3]:  # Top 3 system users
            if user.email:
                recipients.append({
                    'email': user.email,
                    'phone': getattr(user, 'mobile', None)
                })
        
        # Nếu không có system users, lấy current user
        if not recipients and self.env.user.email:
            recipients.append({
                'email': self.env.user.email,
                'phone': getattr(self.env.user, 'mobile', None)
            })
        
        return recipients

    def action_export_report(self):
        """Xuất báo cáo dưới dạng email"""
        # Tạo email
        mail_values = {
            'subject': f'Báo cáo Phân tích Tài sản - {self.analysis_date.strftime("%d/%m/%Y")}',
            'body_html': self._prepare_email_body(),
            'email_to': self.env.user.email,
        }
        
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': 'Báo cáo đã được gửi!',
                'type': 'success',
                'sticky': True,
            }
        }

    def _prepare_email_body(self):
        """Chuẩn bị nội dung email"""
        html = f"""
        <html>
            <body style="font-family: Arial; color: #333;">
                <h2>📊 BÁNG CÁO PHÂN TÍCH TÀI SẢN</h2>
                <p>Ngày: {self.analysis_date.strftime('%d/%m/%Y')}</p>
                
                <h3>📈 Kết quả Phân tích</h3>
                <pre>{self.analysis_text}</pre>
                
                <h3>💡 Khuyến nghị</h3>
                <pre>{self.recommendations}</pre>
                
                <h3>⚠️ Điểm Bất thường</h3>
                <pre>{self.anomalies}</pre>
                
                <hr/>
                <p><small>Email này được tạo tự động bởi hệ thống Odoo.</small></p>
            </body>
        </html>
        """
        return html

    @api.model
    def schedule_monthly_analysis(self):
        """Scheduled Job - chạy hàng tháng để phân tích AI"""
        try:
            # Tạo record phân tích mới
            analysis = self.create({
                'analysis_date': fields.Date.today(),
            })
            
            # Thực hiện phân tích
            analysis.action_analyze()
            
            # Gửi báo cáo qua email
            analysis.action_export_report()
            
            _logger.info(f'Monthly AI analysis completed for {analysis.analysis_date}')
            
        except Exception as e:
            _logger.error(f'Error in monthly AI analysis: {str(e)}')
            # Gửi thông báo lỗi
            self.env['bus.bus']._sendone(
                self.env.user.partner_id, 
                'simple_notification', 
                {
                    'title': 'Lỗi phân tích AI',
                    'message': f'Lỗi phân tích AI hàng tháng: {str(e)}',
                    'sticky': False,  
                    'type': 'danger'  
                }
            )
