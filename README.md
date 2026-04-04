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
## 🔧 Công nghệ sử dụng
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![GitLab](https://img.shields.io/badge/gitlab-%23181717.svg?style=for-the-badge&logo=gitlab&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
    
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

  * **AI Engine:** Google Gemini API (Flash 1.5)
  * **Messaging:** Telegram Bot API

-----


# 🚀 ERP: HỆ THỐNG QUẢN LÝ TÀI SẢN, TÀI CHÍNH

# 1\. Giới thiệu dự án & Những nâng cấp đột phá

## 1.1. Tổng quan

Hệ Thống Quản Lý Tài Sản, Tài Chính không chỉ đơn thuần là một hệ thống quản lý tài sản như các phiên bản tiền nhiệm. Đây là một **Hệ sinh thái ERP thông minh** được phát triển trên nền tảng Odoo 15, tích hợp **Trí tuệ nhân tạo (Generative AI)** và **Hệ thống thông báo đa nền tảng** để tối ưu hóa hiệu suất vận hành doanh nghiệp.

<img width="1024" height="1004" alt="image" src="https://github.com/user-attachments/assets/13f5d3d5-5008-4eb7-a9f7-906c2d659d71" />


## 1.2. Nâng cấp so với hệ thống mẫu (Baseline)

| Đặc điểm | Hệ thống mẫu (TTDN-15-04) | HNDN ERP (Dự án hiện tại) |
| :--- | :--- | :--- |
| **Phạm vi hệ thống** | Quản lý Tài sản đơn lẻ. | **ERP đa phân hệ**: Nhân sự - Tài sản - Tài chính đồng bộ. |
| **Tương tác người dùng** | Giao diện Odoo truyền thống. | **AI Sidebar Chat** (OWL Framework) truy vấn dữ liệu ngôn ngữ tự nhiên. |
| **Thông báo** | Chỉ hiển thị bên trong hệ thống Odoo. | **External API**: Thông báo thời gian thực qua **Telegram Bot**. |
| **Tính nhất quán tài chính** | Khấu hao rời rạc. | **Tự động hóa hạch toán**: Tự sinh bút toán kế toán từ Lương & Khấu hao. |
| **Giao diện Dashboard** | Biểu đồ Odoo mặc định. | **Premium Dashboard**: Custom hoàn toàn bằng thư viện Chart.js & OWL. |

-----

## 1.3. Chi tiết các phân hệ đã nâng cấp

### 🏦 Module Nền tảng AI - [NEW]

Đây là module hoàn toàn mới, đóng vai trò "trạm trung chuyển" cho toàn hệ thống:

  - **AI Service**: Cấu hình kết nối Gemini API, triển khai kỹ thuật **Prompt Engineering** và **Context Injection** giúp Gemini hiểu sâu dữ liệu Odoo.
  - **Telegram Gateway**: Quản lý Bot Token, xử lý gửi thông báo tự động (phiếu lương, đơn mượn tài sản).
  - **AI Chat Logic**: Lưu trữ lịch sử hội thoại và quản lý phiên làm việc (Session) của người dùng.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a33d59f7-f505-4c4f-a960-809caf26b8d9" />


### 👥 Module Nhân sự & Tiền lương - [UPGRADE]

  - **Quản lý Hợp đồng**: Theo dõi vòng đời nhân viên từ lúc thử việc đến khi nghỉ việc.
  - **Chấm công & Tiền lương**: Tự động tính toán bảng lương dựa trên ngày công thực tế.
  - **Chấm công & Tiền lương**: Liên kết trực tiếp với module Tài chính để sinh bút toán chi phí lương tự động khi chốt bảng lương.
<img width="1914" height="574" alt="image" src="https://github.com/user-attachments/assets/3586db48-5d9c-4122-adee-1ee28b994c72" />


### 💻 Module Quản lý Tài sản - [UPGRADE]

  - **Luồng mượn trả**: Số hóa quy trình đề xuất -\> Duyệt -\> Bàn giao.
  - **Tích hợp Telegram**: Gửi tin nhắn xác nhận mượn/trả thiết bị trực tiếp đến nhân viên.
  - **Khấu hao tự động**: Tính toán hao mòn và tự sinh bút toán chi phí khấu hao định kỳ.
  * **Nâng cấp Quy trình**: Không chỉ dừng lại ở mượn/trả, hệ thống tích hợp **Telegram API** để xác nhận mượn tài sản tức thì.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/01c78c81-db6a-4178-a680-e7387a77b89b" />


### 💰 Module Tài chính - [NEW]

  - **Hệ thống sổ cái**: Quản lý bút toán (Journal Entries) tập trung.
  - **Đồng bộ liên module**: Thu thập dữ liệu chi phí từ Nhân sự và Tài sản để lập báo cáo P\&L (Lỗ/Lãi).
  - **Dashboard Tài chính**: Biểu đồ trực quan về dòng tiền và biến động ngân sách.
  * **Hội tụ dữ liệu**: Là nơi tập hợp mọi dòng chảy tiền tệ từ các module khác.
  * **Báo cáo thông minh**: Tự động hóa báo cáo P\&L (Lỗ/Lãi) dựa trên các bút toán được sinh ra tự động từ nghiệp vụ thực tế.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/f2c1ea11-abb9-42b9-b532-bd6b043e6ab5" />

### 📊 Module Trang chủ

  * **Executive Dashboard**: Tổng hợp KPI từ tất cả các module bằng công nghệ OWL.
  * **AI Sidebar Chat**: Trợ lý ảo luôn hiển thị ở cạnh phải màn hình, hỗ trợ truy vấn dữ liệu bằng ngôn ngữ tự nhiên (Ví dụ: "Ai đang giữ máy tính mã TS001?").

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2c8eea2b-3e22-4ccb-b79e-31c4bc0d766d" />



-----

# 2\. Hướng dẫn cài đặt và Thiết lập môi trường

## 2.1. Clone Project

```bash
git clone https://github.com/DoQuangMinh2410/HNQTHTDN-CNTT17-12-N5.git
cd HNQTHTDN-CNTT17-12-N5
```

## 2.2. Cài đặt thư viện hệ thống (Ubuntu 22.04+)

```bash
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-dev build-essential libpq-dev libjpeg-dev zlib1g-dev
```

## 2.3. Khởi tạo môi trường ảo & Cài đặt thư viện Python

```bash
python3.10 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
# Cài đặt thêm thư viện AI & Telegram
pip install google-generativeai python-telegram-bot
```

-----

# 3\. Cấu hình tham số chạy (Quan trọng)

Khác với hệ thống cũ, HNDN ERP yêu cầu các khóa bảo mật API để vận hành tính năng AI:

## 3.1. Cấu hình Gemini & Telegram

Tạo file `.env` hoặc cấu hình trong **System Parameters** của Odoo:

  * `GEMINI_API_KEY`: Lấy tại [Google AI Studio](https://aistudio.google.com/).
  * `TELEGRAM_BOT_TOKEN`: Lấy tại [BotFather](https://t.me/botfather).

## 3.2. File odoo.conf

```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5434
xmlrpc_port = 8069
```

-----

# 4\. Hướng dẫn vận hành & Kiểm tra

Để kiểm tra các tính năng nâng cấp, người dùng thực hiện theo luồng sau:

1.  **Chạy Server**: `python3 odoo-bin -c odoo.conf -u hndn_ai_base,nhan_su,quan_ly_tai_san,quan_ly_tai_chinh,q_trang_chu`
2.  **Test AI Chatbot**: Sử dụng biểu tượng Robot ở Sidebar để hỏi về tài sản hoặc lương.
3.  **Test Telegram**: Thực hiện mượn tài sản và kiểm tra điện thoại có nhận được thông báo.
4.  **Test Tự động hóa Tài chính**: Chốt bảng lương và kiểm tra sổ nhật ký chung trong module Tài chính.

-----


## 📚 Tài liệu tham khảo

  - https://github.com/nguyenngocdantruong/TTDN-15-04-N6.git
