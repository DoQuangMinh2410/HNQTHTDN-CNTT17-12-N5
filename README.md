# HNDN ERP System - Giải pháp Quản trị Doanh nghiệp Thông minh

Hệ thống ERP HNDN là một giải pháp quản trị doanh nghiệp toàn diện được xây dựng trên nền tảng Odoo, tích hợp Trí tuệ nhân tạo (Gemini AI) và thông báo tức thời qua Telegram để tối ưu hóa quy trình vận hành.

## 🌟 Tính năng nổi bật

- **Trợ lý ảo AI**: Sidebar trò chuyện tích hợp AI Gemini (Google), có khả năng ghi nhớ lịch sử và gợi ý nghiệp vụ thông minh.
- **Tự động hóa thông báo**: Tích hợp Telegram Bot gửi tin nhắn tự động khi Duyệt lương, Duyệt mua sắm, Mượn/Trả tài sản.
- **AI OCR**: Tự động bóc tách dữ liệu từ file CV (PDF/Ảnh) phục vụ tuyển dụng.
- **Hạch toán tự động**: Kết nối dữ liệu từ Nhân sự và Tài sản sang Kế toán một cách tự động và chính xác.

## 📂 Cấu trúc Module

Dự án bao gồm 4 module chính:

### 1. [hndn_ai_base](addons/hndn_ai_base)
Cung cấp nền tảng AI và Messenger. Chứa các tiện ích dùng chung để kết nối Gemini API và Telegram API.

### 2. [nhan_su](addons/nhan_su)
Quản trị nguồn nhân lực. Bao gồm: Hồ sơ nhân viên, Bảng lương, Hợp đồng lao động, Nghỉ phép và Khen thưởng kỷ luật.

### 3. [quan_ly_tai_san](addons/quan_ly_tai_san)
Quản lý vòng đời tài sản. Bao gồm: Danh mục tài sản, Khấu hao tự động, Mượn/Trả tài sản, Bảo trì và Mua sắm.

### 4. [quan_ly_tai_chinh](addons/quan_ly_tai_chinh)
Quản trị tài chính kế toán. Bao gồm: Bút toán kế toán, Hệ thống tài khoản, Quản lý Tạm ứng và Báo cáo P&L (Lợi nhuận).

## 🛠 Công nghệ sử dụng

- **Odoo Framework**: Nền tảng ERP core.
- **Python**: Xử lý logic nghiệp vụ và tích hợp API.
- **Owl (Odoo Web Library)**: Xây dựng giao diện AI Chat sidebar hiện đại.
- **Google Gemini API**: Động cơ AI phân tích dữ liệu và trò chuyện.
- **Telegram Bot API**: Hệ thống thông báo thời gian thực miễn phí.

## 🚀 Hướng dẫn thiết lập nhanh

1. **Cấu hình AI**: Truy cập **Nhân sự > Công nghệ mới > Cấu hình hệ thống**.
2. **Setup Gemini**: Nhập Gemini API Key từ Google AI Studio.
3. **Setup Telegram**: Nhập Bot Token từ @BotFather và Chat ID của người nhận. Sau đó nhấn **"Kiểm tra kết nối"** để kích hoạt.

---
*Phát triển bởi đội ngũ HNDN-CNTT17-12-N5*
