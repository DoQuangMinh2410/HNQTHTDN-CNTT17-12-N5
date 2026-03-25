# Quan Ly Tai Chinh - Module Quản lý Tài chính & Kế toán

Module này quản lý các sổ sách kế toán, hạch toán tự động và báo cáo kết quả kinh doanh.

## Tính năng chính

### 1. Quản lý Bút toán Kế toán
- Ghi nhận các phát sinh Nợ/Có theo hệ thống tài khoản chuẩn.
- **Tự động hóa**: Nhận dữ liệu hạch toán tự động từ module Bảng lương (Nhân sự) và Khấu hao tài sản (Tài sản).

### 2. Quản lý Tạm ứng & Hoàn ứng
- Theo dõi các khoản tạm ứng của nhân viên cho các hoạt động công tác hoặc mua sắm lẻ.
- Quy trình phê duyệt và tất toán khoản tạm ứng minh bạch.

### 3. Hệ thống Báo cáo
- **Báo cáo P&L (Lợi nhuận)**: Tự động tổng hợp doanh thu và chi phí để tính toán hiệu quả kinh doanh.
- **AI Analytics**: Tích hợp với Gemini để cung cấp các phân tích dữ liệu tài chính thông minh qua trợ lý ảo.

## Kỹ thuật
- **Model chính**: `but_toan`, `tai_khoan_ke_toan`, `tam_ung`, `bao_cao`.
- **Phụ thuộc**: `base`, `nhan_su`, `quan_ly_tai_san`.
