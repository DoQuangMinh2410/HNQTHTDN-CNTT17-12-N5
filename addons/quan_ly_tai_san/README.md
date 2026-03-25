# Quan Ly Tai San - Module Quản lý Tài sản Doanh nghiệp

Module này cung cấp giải pháp toàn diện để theo dõi vòng đời tài sản từ lúc mua đến khi thanh lý.

## Tính năng chính

### 1. Quản trị Danh mục Tài sản
- Quản lý thông tin chi tiết: Loại tài sản, nguyên giá, giá trị khấu hao hàng tháng.
- **Tự động hóa khấu hao**: Hệ thống tự động tính toán và cập nhật giá trị hiện tại của tài sản mỗi tháng.
- **Phân bổ tài sản**: Ghi nhận tài sản đang được sử dụng tại phòng ban nào.

### 2. Quy trình Mượn & Trả Tài sản
- **Đơn mượn tài sản**: Quy trình phê duyệt mượn tài sản giữa các phòng ban.
- **Phiếu mượn/trả**: Ghi nhận thực tế việc bàn giao và hoàn trả.
- **Thông báo Telegram**: Tự động gửi tin nhắn báo mượn thành công hoặc xác nhận đã trả tài sản xong.

### 3. Bảo trì & Kiểm kê
- **Lập kế hoạch bảo trì**: Theo dõi lịch bảo dưỡng định kỳ để đảm bảo tài sản hoạt động tốt.
- **Kiểm kê tài sản**: Đối soát định kỳ để phát hiện thất thoát hoặc hư hỏng.

### 4. Yêu cầu Mua sắm
- Chức năng đề xuất mua mới tài sản khi có nhu cầu.
- **Automation**: Khi duyệt mua, hệ thống tự động khởi tạo bản ghi Tài sản mới và gửi thông báo Telegram.

## Kỹ thuật
- **Model chính**: `tai_san`, `phan_bo_tai_san`, `muon_tra_tai_san`, `yeu_cau_mua_sam`, `bao_tri_tai_san`.
- **Phụ thuộc**: `base`, `nhan_su`, `hndn_ai_base`.
