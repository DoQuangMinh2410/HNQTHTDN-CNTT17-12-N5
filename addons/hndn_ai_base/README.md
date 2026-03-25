# HNDN AI Base - Module Nền tảng AI & Thông báo

Module này cung cấp các tiện ích nền tảng cho việc tích hợp Trí tuệ nhân tạo (AI) và hệ thống thông báo qua Telegram cho toàn bộ hệ sinh thái HNDN.

## Tính năng chính

### 1. Trợ lý ảo AI (Gemini)
- **Sidebar AI Chat**: Tích hợp thanh trò chuyện trực diện trong giao diện Odoo.
- **Lịch sử hội thoại**: Tự động lưu và quản lý các luồng chat theo phiên (Session).
- **Gợi ý thông minh**: Sau mỗi câu trả lời, AI tự động gợi ý 3-4 câu hỏi liên quan đến các nghiệp vụ Nhân sự, Tài sản, Tài chính để người dùng thao tác nhanh.
- **Bối cảnh nghiệp vụ**: AI được cung cấp thông tin thực tế từ cơ sở dữ liệu (Bảo hành tài sản, Thông tin nhân viên, v.v.) để trả lời chính xác nhất.

### 2. Tiện ích AI Messenger
- **Cổng kết nối Gemini API**: Xử lý gửi/nhận dữ liệu từ Google Gemini Flash Latest.
- **Cổng kết nối Telegram Bot**: Cung cấp API nội bộ cho các module khác gửi thông báo tự động (Duyệt lương, Duyệt mua sắm, Mượn/Trả tài sản).

## Cấu hình
Người quản trị cần cấu hình các thông số sau tại **Cấu hình > Cài đặt > HNDN AI Base**:
- **Gemini API Key**: Token lấy từ Google AI Studio.
- **Telegram Bot Token**: Token từ @BotFather.
- **Telegram Chat ID**: ID người nhận thông báo mặc định.

## Kỹ thuật
- **Model chính**: `ai_assistant`, `ai_chat_message`
- **Utility**: `AIMessengerUtils` (Lớp static dùng chung cho toàn bộ hệ thống).
- **Frontend**: Sử dụng Owl Framework để xây dựng Chat UI linh hoạt.
