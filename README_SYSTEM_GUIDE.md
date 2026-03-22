# 🎯 Hệ Thống Quản Lý Tài Sản Odoo 15

## 📋 Tổng Quan

Hệ thống gồm 3 module chính:

1. **HRM Extension** - Quản lý nhân viên và gán tài sản
2. **Asset Management** (quan_ly_tai_san) - Quản lý tài sản
3. **Accounting Module** - Quản lý khấu hao và kế toán

## 📦 Cài Đặt

### Bước 1: Kích hoạt Modules

```bash
# Trong Odoo:
# 1. Đi đến Apps
# 2. Cài đặt các module theo thứ tự:
#    - nhan_su (HR)
#    - quan_ly_tai_san (Asset Management)
#    - hrm_extension (HR Extension)
#    - accounting_module (Accounting)
```

### Bước 2: Tải Demo Data (Tùy chọn)

```bash
# Khi cài đặt, chọn "Load Demo Data" để tải dữ liệu mẫu
# Dữ liệu demo sẽ tạo:
# - 2 nhân viên mẫu
# - 2 tài sản mẫu
# - 2 lịch khấu hao mẫu
```

## 🔄 Luồng Dữ Liệu

```
┌─────────────────────────────────────────────────────────────┐
│                    LUỒNG HỆ THỐNG                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Tạo Nhân viên (HRM)                                    │
│           ↓                                                 │
│  2. Tạo Tài sản (Asset Management)                         │
│           ↓                                                 │
│  3. Gán Nhân viên vào Tài sản (HRM Extension)              │
│           ↓                                                 │
│  4. Xác nhận Tài sản → In Use (Asset Management)           │
│           ↓                                                 │
│  5. Tự động tạo Lịch khấu hao (Accounting)               │
│           ↓                                                 │
│  6. Tự động tạo Khấu hao từng tháng (Cron Job)           │
│           ↓                                                 │
│  7. Tự động tạo Bút toán kế toán (Accounting)            │
│           ↓                                                 │
│  8. Chạy AI Phân tích (Accounting)                        │
│                                                            │
└─────────────────────────────────────────────────────────────┘
```

## 👤 Quản Lý Nhân Viên

### Tạo Nhân viên

```
Đường dẫn: HR → Nhân viên → Tạo
Điền:
  - Mã định danh (ví dụ: NV001)
  - Họ tên
  - Ngày sinh
  - Email, Số điện thoại
```

## 🏢 Quản Lý Tài Sản

### Tạo Tài sản

```
Đường dẫn: Quản Lý Tài Sản → Tài Sản → Tạo
Điền:
  - Mã tài sản (ví dụ: TS001)
  - Tên tài sản
  - Ngày mua
  - Giá trị ban đầu
  - Loại tài sản
  - Phương pháp khấu hao: "Tuyến tính" hoặc "Giảm dần"
  - Thời gian sử dụng (năm)
  - Chọn nhân viên được giao (Nhân viên được giao)
```

### Xác Nhận Tài Sản

```
1. Từ form tài sản, nhấn nút "Xác nhận"
2. Hệ thống sẽ:
   ✓ Chuyển trạng thái → "Đang sử dụng"
   ✓ Tự động tạo Lịch khấu hao
   ✓ Tạo các bản ghi khấu hao cho từng tháng
```

## 💰 Quản Lý Kế Toán

### Khấu hao Tài Sản

```
Đường dẫn: Kế toán → Khấu hao → Danh sách Khấu hao

Trạng thái:
  - Nháp: Bản ghi mới tạo
  - Xác nhận: Khấu hao được xác nhận
  - Đã ghi sổ: Bút toán đã được ghi nhận

Quy trình:
1. Hệ thống tự động tạo khấu hao hàng tháng (Cron Job)
2. Nhấn "Xác nhận" để xác nhận khấu hao
3. Nhấn "Ghi sổ" để ghi nhận bút toán
```

### Công Thức Tính Khấu Hao

#### Khấu hao Tuyến tính (Straight-line):

```
Khấu hao hàng tháng = Giá trị ban đầu / Thời gian sử dụng (tháng)

Ví dụ: Máy tính 25 triệu, sử dụng 5 năm (60 tháng)
Khấu hao/tháng = 25.000.000 / 60 = 416.667 VNĐ
```

#### Khấu hao Giảm dần (Degressive):

```
Khấu hao hàng tháng = Giá trị hiện tại × Tỷ lệ khấu hao (%)

Ví dụ: 25 triệu, tỷ lệ 20%/năm (~1.67%/tháng)
Tháng 1: 25.000.000 × 1.67% = 417.500 VNĐ
Tháng 2: 24.582.500 × 1.67% = 410.328 VNĐ (giảm dần)
```

### Bút Toán Kế Toán

```
Đường dẫn: Kế toán → Bút toán → Danh sách Bút toán

Khi khấu hao được xác nhận:
  ✓ Tự động tạo bút toán lên tài khoản khấu hao
  ✓ Ghi nhận số tiền khấu hao để tháng

Các loại bút toán:
  - Khấu hao: Khấu hao định kỳ
  - Thanh lý: Khi tài sản được thanh lý
  - Điều chỉnh: Điều chỉnh giá trị tài sản
```

## 🤖 Tính Năng AI & Phân Tích

### Phân Tích AI Tài Sản

```
Đường dẫn: Kế toán → AI & Báo cáo → Phân tích AI Tài sản

Chức năng:
  1. Tạo bẩu ghi phân tích mới
  2. Nhấn "Chạy Phân tích" để phân tích
  3. Kết quả sẽ hiển thị:
     ✓ Tổng thống kê: Số tài sản, Giá trị, Khấu hao trung bình
     ✓ Phân loại: Tài sản đang sử dụng, hư hỏng
     ✓ Khuyến nghị: Các đề xuất tối ưu
     ✓ Điểm bất thường: Tài sản cần chú ý

  4. Nhấn "Xuất Báo cáo" để gửi email báo cáo
```

### Báo Cáo Tự Động

```
Hệ thống sẽ gửi email báo cáo:
  - Nội dung: Phân tích, khuyến nghị, điểm bất thường
  - Định dạng: HTML đẹp mắt
```

## ⏰ Scheduled Jobs (Cron)

### Tạo Khấu hao Hàng Tháng

```
Tự chạy: Hàng tháng vào ngày 1

Chức năng:
  1. Tìm tất cả tài sản "Đang sử dụng"
  2. Kiểm tra xem tháng hiện tại đã có khấu hao chưa
  3. Nếu chưa → Tạo khấu hao mới
  4. Tự động tạo bút toán kế toán

Có thể chạy thủ công:
  - Từ form tài sản: Nút "Tạo Khấu hao"
```

## 📊 Gán Tài Sản cho Nhân Viên

### Tạo Gán Tài Sản

```
Đường dẫn: HR Mở rộng → Gán Tài sản → Tạo

Điền:
  - Chọn Tài sản
  - Chọn Nhân viên
  - Ngày gán (tự động: hôm nay)
  - Ghi chú

Trạng thái:
  - Đã gán: Nhân viên đang sử dụng
  - Đã thu hồi: Tài sản được trả lại
  - Hư hỏng: Tài sản bị hư hỏng
```

### Xem Tài Sản của Nhân Viên

```
Đường dẫn: HR → Nhân Viên → [Chọn Nhân viên]

Trong form Nhân viên, tab "Tài sản được giao":
  ✓ Danh sách tất cả tài sản được giao
  ✓ Ngày gán, Trạng thái
```

## 🧪 Demo Flow (Kiểm Tra Toàn Bộ System)

### Bước 1: Chuẩn bị Demo Data

```bash
# 1. Khi cài accounting_module, chọn "Load Demo Data"
# Hệ thống sẽ tạo:
#    ✓ 2 nhân viên (Nguyễn Văn A, Trần Thị B)
#    ✓ 2 tài sản (Laptop, Bàn làm việc)
#    ✓ 2 lịch khấu hao
```

### Bước 2: Kiểm Tra Dữ Liệu

```
1. HR → Nhân Viên:
   ✓ Thấy 2 nhân viên mẫu

2. Quản Lý Tài Sản → Tài Sản:
   ✓ Thấy 2 tài sản với trạng thái "Nháp"
   ✓ Mỗi tài sản gán với một nhân viên
   ✓ Có phương pháp khấu hao "Tuyến tính"
```

### Bước 3: Xác Nhận Tài Sản

```
1. Mở tài sản "Laptop Dell XPS 13"
2. Nhấn nút "Xác nhận"
3. Kết quả:
   ✓ Trạng thái → "Đang sử dụng"
   ✓ Tự động tạo Lịch khấu hao
   ✓ Tạo các bản ghi khấu hao cho 60 tháng (5 năm)
```

### Bước 4: Xem Khấu hao

```
1. Kế toán → Khấu hao → Danh sách Khấu hao
2. Thấy danh sách khấu hao:
   ✓ Date, Asset, Employee, Depreciation Amount
   ✓ Trạng thái "Nháp"
```

### Bước 5: Xác Nhận Khấu hao

```
1. Mở khấu hao tháng 1
2. Nhấn "Xác nhận"
3. Kết quả:
   ✓ Trạng thái → "Xác nhận"
   ✓ Nhấn "Ghi sổ"
   ✓ Trạng thái → "Đã ghi sổ"
   ✓ Bút toán kế toán được tạo tự động
```

### Bước 6: Xem Bút Toán

```
1. Kế toán → Bút toán → Danh sách Bút toán
2. Thấy bút toán vừa tạo:
   ✓ Asset: Laptop Dell XPS 13
   ✓ Amount: 416.667 VNĐ
   ✓ Date: 01/01/2023
   ✓ State: Đã ghi sổ
```

### Bước 7: Chạy AI Phân Tích

```
1. Kế toán → AI & Báo cáo → Phân tích AI Tài sản
2. Nhấn "Tạo"
3. Nhấn "Chạy Phân tích"
4. Xem kết quả:
   ✓ Tổng 2 tài sản, Giá trị 30 triệu
   ✓ Khấu hao trung bình
   ✓ Khuyến nghị tối ưu
5. Nhấn "Xuất Báo cáo" để gửi email
```

### Bước 8: Gán Tài Sản (HR Extension)

```
1. HR Mở rộng → Gán Tài sản → Tạo
2. Chọn:
   ✓ Tài sản: Laptop
   ✓ Nhân viên: Nguyễn Văn A
   ✓ Ngày gán: Hôm nay
3. Nhấn "Lưu"
4. Kiểm tra:
   - HR → Nhân viên → Nguyễn Văn A
   - Tab "Tài sản được giao" → Thấy Laptop
```

### Bước 9: Kiểm Tra Gán Tài Sản

```
1. HR → Nhân Viên → Nguyễn Văn A
2. Tab "Tài sản được giao":
   ✓ Thấy Laptop
   ✓ Ngày gán: (hôm nay)
   ✓ Trạng thái: Đã gán
```

## 🔧 Customization

### Thêm Phương Pháp Khấu hao Mới

Sửa `asset_depreciation_schedule.py`:

```python
depreciation_method = fields.Selection([
    ('straight_line', 'Tuyến tính'),
    ('degressive', 'Giảm dần'),
    ('sum_of_digits', 'Sum-of-digits'),  # Thêm mới
])
```

### Thay Đổi Công Thức Khấu hao

Sửa `_compute_monthly_depreciation()` hoặc `_perform_local_analysis()`.

### Thêm External API

Sửa `asset_ai_analysis.py` - add `requests` para gọi API bên ngoài.

## 📧 Email Integration

```
1. Cấu hình Send Mail Setup:
   Settings → Technical → Email Configuration

2. Tài khoản SMTP:
   Gmail hoặc Provider khác

3. Các phương thức gửi email:
   - Báo cáo AI được gửi tự động
   - Tút toán được gửi nếu cấu hình thêm
```

## 🐛 Troubleshooting

### Khấu hao không được tạo tự động

```
1. Kiểm tra:
   - Tài sản có trạng thái "Đang sử dụng"?
   - Phương pháp khấu hao ≠ "Không"?
   - Lịch khấu hao đã tạo?

2. Chạy cron thủ công:
   - Kế toán → Scheduled Actions
   - Tìm "Generate Monthly Depreciation"
   - Nhấn "Chạy Ngay"
```

### Bút toán không được tạo

```
1. Kiểm tra:
   - Khấu hao có trạng thái "Xác nhận"?
   - Email setup đã cấu hình?

2. Manual create:
   - Kế toán → Bút toán → Tạo
   - Điền thông tin tương ứng
```

## 📞 Hỗ Trợ

Liên hệ: ttdn.team@example.com
