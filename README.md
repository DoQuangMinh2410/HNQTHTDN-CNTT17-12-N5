<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
    Youth Union Member Management
</h2>
<div align="center">
    <p align="center">
        <img width="170" alt="image" src="https://github.com/user-attachments/assets/e5cf9d51-47fb-42d2-b5df-fb3d2e669772" />
        <img width="180"  alt="image" src="https://github.com/user-attachments/assets/1a21a890-24d3-4481-b8ca-7885637bf17e" />
        <img width="200" alt="image" src="https://github.com/user-attachments/assets/4901129c-be54-4246-9478-2847c45a48bd" />
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

---
## 🔧 Các công nghệ được sử dụng

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
    
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)




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
