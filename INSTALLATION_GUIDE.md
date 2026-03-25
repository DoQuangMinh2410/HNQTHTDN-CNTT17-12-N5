# 🚀 INSTALLATION & SETUP GUIDE

## 📋 Hệ Thống Yêu Cầu

- **Odoo Version**: 15.0
- **Python**: 3.8+
- **Database**: PostgreSQL 12+
- **Dependencies**: Đã được liệt kê trong `requirements.txt`

## 🔧 Cài Đặt Nhanh

### 1. Download & Extract

```bash
# Nếu chưa có project
git clone <repository>
cd TTDN-15-04-N6-main
```

### 2. Cài Đặt Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Tạo Database (Nếu chưa có)

```bash
createdb -U postgres odoo15_asset_system
```

### 4. Chạy Odoo Server

```bash
# Khởi động server
python odoo-bin -c odoo.conf --dev=all

# Hoặc với custom config
python odoo-bin.py -c odoo.conf.template \
  --db_host=localhost \
  --db_user=postgres \
  --db_password=postgres \
  --db_port=5432 \
  --addons-path=addons
```

### 5. Truy Cập Odoo

```
URL: http://localhost:8069
Username: admin
Password: admin
```

## 📦 Cài Đặt Modules

### Bước 1: Kích Hoạt Modules Cơ Bản

```
1. Đăng nhập vào Odoo
2. Đi đến: Apps → Updates → Update Module List
3. Cài đặt các module theo thứ tự:
```

**Thứ tự cài đặt:**

| #   | Module              | Tên Tiếng Việt  | Mô Tả                               |
| --- | ------------------- | --------------- | ----------------------------------- |
| 1   | `nhan_su`           | Nhân Sự         | Quản lý nhân viên (có sẵn)          |
| 2   | `quan_ly_tai_san`   | Quản Lý Tài Sản | Quản lý tài sản (có sẵn, đã update) |
| 3   | `hrm_extension`     | HRM Mở Rộng     | Gán tài sản cho nhân viên (MỚI)     |
| 4   | `accounting_module` | Kế Toán         | Khấu hao & kế toán (MỚI)            |

### Cài Đặt Từng Module

#### Bước 2.1: Cài nhan_su

```
Apps → Search "nhan_su" → Install
```

#### Bước 2.2: Cài quan_ly_tai_san (with update)

```
Apps → Search "quan_ly_tai_san" → Update (hoặc Install nếu mới)
```

#### Bước 2.3: Cài hrm_extension

```
Apps → Search "hrm_extension" → Install
```

✅ **Dự kiến:** Module sẽ load vào `HR` menu

#### Bước 2.4: Cài accounting_module

```
Apps → Search "accounting_module" → Install
```

✅ **Dự kiến:** Module sẽ load vào `Accounting` menu mới

### Bước 3: Tải Demo Data

**Option A: Tải trong quá trình cài đặt**

```
1. Khi cài accounting_module
2. Nếu được hỏi "Load Demo Data?" → Chọn "YES"
3. Hệ thống sẽ tạo tự động:
   - 2 nhân viên mẫu
   - 2 tài sản mẫu
   - 2 lịch khấu hao
```

**Option B: Tải manual sau**

```
1. Apps → Accounting Module → Demo Data → Load Examples
2. Hoặc: Admin → Load Demo Data
```

### Bước 4: Xác Nhận Cài Đặt

```
1. Menu Projects → Tìm các menu mới:
   ✓ HR → HR Mở rộng → Gán Tài sản
   ✓ Kế toán → Khấu hao / Bút toán / AI & Báo cáo

2. Kiểm tra dữ liệu:
   ✓ HR → Nhân Viên → Thấy nhân viên mẫu
   ✓ Quản Lý Tài Sản → Tài Sản → Thấy tài sản mẫu
```

## ⚙️ Cấu Hình Email (SMTP)

### Tại sao cần cấu hình?

- Gửi báo cáo tự động
- Thông báo hệ thống
- Multi-user notifications

### Các Bước Cấu Hình

#### 1. Đi đến Email Settings

```
Admin Center (Settings icon) → Users & Companies → Email Configuration
```

Hoặc:

```
Settings → Technical → Email → Outgoing Mail Servers
```

#### 2. Tạo Email Server

**Cho Gmail:**

```
Form Fields:
  - Name: Gmail SMTP
  - SMTP server: smtp.gmail.com
  - SMTP Port: 587
  - Username: your-email@gmail.com
  - Password: your-app-password (NOT regular password)
  - Security: TLS
  - Active: ✓

Lưu ý Gmail:
  1. Cần bật "Less secure app access" HOẶC
  2. Tạo "App Password" (recommended)
     → Google Account → Security → App Passwords
```

**Cho SendGrid hoặc Provider khác:**

```
Xem documentation của provider:
  - SMTP Hostname
  - Port (usually 587 or 465)
  - API Key (as password)
```

#### 3. Test Connection

```
Nhấn nút "Test Connection"
  → Nếu thành công: ✓ Connection Successful
```

## 🧪 Quick Test - Demo Flow

### Scenario: Test toàn bộ hệ thống trong 5 phút

#### Step 1: Tạo Nhân Viên (nếu chưa có demo data)

```
HR → Nhân Viên → Tạo
  - Mã: NV_TEST_001
  - Tên: Test Employee
  - Email: test@example.com
  - Lưu
```

#### Step 2: Tạo Tài Sản

```
Quản Lý Tài Sản → Tài Sản → Tạo
  - Mã: TS_TEST_001
  - Tên: Test Computer
  - Ngày mua: 01/01/2023
  - Giá trị: 10,000,000 VNĐ
  - Loại: Máy tính
  - Phương pháp: Tuyến tính
  - Thời gian: 5 năm
  - Nhân viên: Test Employee
  - Lưu
```

#### Step 3: Xác Nhận Tài Sản

```
Từ form tài sản → Nhấn nút "Xác nhận"
  → Trạng thái: Draft → Đang sử dụng
  → Tự động tạo 60 khấu hao (5 năm × 12 tháng)
```

#### Step 4: Xem Khấu Hao

```
Kế toán → Khấu hao → Danh sách Khấu hao
  → Thấy 60 bản ghi khấu hao
  → Trạng thái: Nháp
```

#### Step 5: Xác Nhận Khấu Hao (tháng 1)

```
Mở khấu hao tháng 1 → Nhấn "Xác nhận"
  → Nhấn "Ghi sổ"
  → Trạng thái: Đã ghi sổ
```

#### Step 6: Xem Bút Toán

```
Kế toán → Bút toán → Danh sách Bút toán
  → Thấy bút toán vừa tạo
  → Amount = 10,000,000 / 60 = 166,666.67 VNĐ
```

#### Step 7: Chạy AI Phân Tích

```
Kế toán → AI & Báo cáo → Phân tích AI Tài sản
  → Tạo → Chạy Phân tích
  → Xem kết quả
  → Xuất Báo cáo (gửi email nếu cấu hình)
```

#### Step 8: Gán Tài Sản

```
HR Mở rộng → Gán Tài sản → Tạo
  - Tài sản: Test Computer
  - Nhân viên: Test Employee
  - Ngày gán: (hôm nay)
  - Lưu
```

#### Step 9: Kiểm Tra HR Record

```
HR → Nhân Viên → Test Employee
  → Tab "Tài sản được giao"
  → Thấy Test Computer
```

✅ **Hoàn tất!** System hoạt động bình thường.

## 🔄 Scheduled Jobs Management

### Xem Scheduled Jobs

```
Admin Center → Technical → Automation → Scheduled Actions
```

### Monthly Depreciation Job

```
Tìm: "Generate Monthly Depreciation"

Settings:
  - Model: asset.depreciation.schedule
  - Frequency: Monthly
  - Next Execution: (tự động tính)
  - Active: ✓

Manual Trigger:
  - Nhấn "Run Now" để chạy ngay
```

### Debug Scheduled Job

```
Nếu Cron không chạy:
  1. Kiểm tra: Active = ✓
  2. Nhấn "Run Now" để test
  3. Kiểm tra logs: /var/log/odoo (nếu production)
  4. Đảm bảo server đang chạy background workers
```

## 📊 Database Troubleshooting

### Reset Database

```bash
# Xóa database
dropdb -U postgres odoo15_asset_system

# Tạo lại
createdb -U postgres odoo15_asset_system

# Khởi động lại server
python odoo-bin -c odoo.conf --dev=all
```

### Backup Database

```bash
# Backup
pg_dump -U postgres odoo15_asset_system > backup.sql

# Restore
psql -U postgres odoo15_asset_system < backup.sql
```

## 🔐 Security Setup

### User Roles

```
1. User (Standard):
   - Read, Write, Create depreciation
   - Cannot Delete
   - View own assignments

2. System (Manager):
   - Full access
   - Can Delete
   - Can configure system
```

### Change User Role

```
Settings → Users & Security → Users
  → Select User
  → Groups: Change/Add groups
```

## 🐛 Troubleshooting Common Issues

### Issue: Module không hiện trong Apps

**Solution:**

```
1. Apps → Updates → Update Modules
2. Tìm module cụ thể
3. Nếu không thấy → Check module folder:
   /addons/accounting_module/__manifest__.py (exists?)
4. Restart server
```

### Issue: ValueError - Object has no attribute

**Solution:**

```
1. Check if field exists in model
2. Check XML inheritance path
3. Restart server with --dev=all
4. Check logs for detailed error
```

### Issue: Depreciation không tạo

**Solution:**

```
1. Verify: usage_status = 'in_use'? ✓
2. Verify: pp_khau_hao ≠ 'none'? ✓
3. Verify: depreciation_schedule_id exists? ✓
4. Run: Assets → action_confirm() manually
5. Check: Logs for errors
```

### Issue: Email không gửi

**Solution:**

```
1. Test SMTP connection (tại Email Servers)
2. Verify: email address valid?
3. Check firewall: Port 587 open?
4. Check: Outgoing mail queue (Mail → Outgoing Mail)
5. Verify: user has email in profile
```

## 📚 Additional Resources

- **User Guide**: [README_SYSTEM_GUIDE.md](README_SYSTEM_GUIDE.md)
- **Technical Docs**: [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
- **Odoo Documentation**: https://docs.odoo.com/15.0/

## 📞 Support

Trong trường hợp gặp vấn đề:

1. **Check Logs:**

   ```bash
   # Development mode logs
   tail -f /var/log/odoo.log

   # Or check browser console (F12)
   ```

2. **Enable Debug Mode:**

   ```
   Settings → Developer Tools → Activate Debug Mode
   ```

3. **Contact Support:**
   - Email: ttdn.team@example.com
   - Issue: Create GitHub issue with logs

## ✅ Verification Checklist

Trước khi declare "Ready for Production":

```
[ ] 1. Tất cả 4 modules installed
[ ] 2. Demo data loaded
[ ] 3. Email configuration working
[ ] 4. Test flow hoàn tất thành công
[ ] 5. Scheduled jobs active
[ ] 6. User roles configured
[ ] 7. Database backed up
[ ] 8. Documentation reviewed
[ ] 9. System tested in production domain
[ ] 10. Users trained
```

---

**Chúc bạn cài đặt thành công!** 🎉
