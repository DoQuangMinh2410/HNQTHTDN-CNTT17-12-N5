# Nhan Su - Module Quản lý Nhân sự & Tổng hợp

Module này trung tâm hóa dữ liệu nhân viên và tự động hóa các quy trình trả lương, nghỉ phép, hợp đồng.

## Tính năng chính

### 1. Quản lý Hồ sơ Nhân viên
- Lưu trữ thông tin cá nhân, liên hệ, học vấn, lịch sử công tác.
- **AI OCR CV**: Tự động bóc tách dữ liệu từ file CV tải lên bằng Gemini AI.
- **Ràng buộc thông minh**: Hệ thống tự động cảnh báo nếu nhân viên nghỉ việc mà còn tài sản đang mượn chưa trả.

### 2. Quản lý Bảng tính lương
- Tự động lấy dữ liệu từ Hợp đồng (Lương cơ bản) và Chấm công (Hệ số công).
- **Automation**: Khi duyệt bảng lương, hệ thống tự động sinh bút toán kế toán (Tài chính) và gửi thông báo Telegram cho nhân viên.

### 3. Quy trình khác
- **Đơn nghỉ phép**: Quản lý lịch nghỉ và tính toán phép năm.
- **Hợp đồng lao động**: Theo dõi thời hạn và các điều khoản lương.
- **Khen thưởng & Kỷ luật**: Lưu trữ hồ sơ thành tích và vi phạm.

## Cấu hình
- Tích hợp cấu hình Telegram Bot tại **Cấu hình > Cài đặt > Nhân Sự & Thông Báo**.
- **Kiểm tra kết nối**: Cung cấp nút bấm test Bot ngay từ giao diện cấu hình.

## Kỹ thuật
- **Model chính**: `nhan_vien`, `tinh_luong`, `hop_dong`, `phep_nam`, `res_config_settings`.
- **Phụ thuộc**: `base`, `quan_ly_tai_chinh`, `hndn_ai_base`.
