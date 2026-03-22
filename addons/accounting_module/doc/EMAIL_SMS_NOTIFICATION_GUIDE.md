# Hướng dẫn Tích hợp Email/SMS Notification API

## Tổng quan

Module Accounting cung cấp khả năng gửi thông báo qua Email (Gmail, SMTP, SendGrid) và SMS (Viettel, Twilio, AWS SNS) tự động khi:

- ✅ Khấu hao định kỳ hoàn thành
- ✅ Phát hiện bất thường trong dữ liệu
- ✅ Tài sản sắp hết niên hạn

## Kiến trúc

```
Notification Flow:
┌─────────────────────────────────────────────────────────┐
│ Event Triggered                                             │
│ (Depreciation/Anomaly/Asset Expiration)                 │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Create Notification Log Entry                               │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ Notification Service                                        │
│ - Load Active Configurations                            │
│ - Format Email/SMS Content                              │
│ - Call Provider API                                     │
└────────────────────┬────────────────────────────────────┘
                     ↓
        ┌────────────┴────────────┐
        ↓                         ↓
    ┌────────┐            ┌────────────┐
    │ Email  │            │ SMS        │
    └────────┘            └────────────┘
        ├─ Gmail              ├─ Viettel
        ├─ SMTP               ├─ Twilio
        └─ SendGrid           └─ AWS SNS
```

## Cấu hình Email

### 1. Gmail API (Khuyến nghị)

#### 1.1 Tạo Google Cloud Project

1. Truy cập: https://console.cloud.google.com
2. Tạo project mới: **Accounting Notifications**
3. Bật Gmail API: **APIs & Services** → **Enable APIs and Services** → Search **Gmail API** → **Enable**

#### 1.2 Tạo Service Account

1. Vào: **APIs & Services** → **Credentials**
2. Nhấp **Create Credentials** → **Service Account**
3. Điền:
   - Service account name: `accounting-notifications`
   - Description: `For sending accounting notifications`
4. Nhấp **Create**

#### 1.3 Tạo JSON Key

1. Vào **Service Accounts** → Chọn account vừa tạo
2. Tab **Keys** → **Add Key** → **Create new key**
3. Chọn **JSON** → **Create**
4. File JSON sẽ được download

#### 1.4 Cấu hình trong Odoo

1. Vào: **Accounting** → **Cấu hình Thông báo** → **Email**
2. Tạo cấu hình mới:
   ```
   Tên: Gmail Production
   Nhà cung cấp Email: Gmail API
   Email gửi từ: your-email@gmail.com
   ```
3. Dán nội dung file JSON vào **Gmail Service Account JSON**
4. Nhấp **Test Kết nối**

**Lưu ý**: Email `your-email@gmail.com` phải trùng với email trong file Service Account JSON

### 2. SMTP Server

#### 2.1 Cấu hình trong Odoo

1. Vào: **Accounting** → **Cấu hình Thông báo** → **Email**
2. Tạo cấu hình mới:
   ```
   Tên: SMTP Company
   Nhà cung cấp Email: SMTP Server
   SMTP Host: mail.company.com
   SMTP Port: 587
   Username: your-email@company.com
   Password: your-password
   Sử dụng TLS: ✓ Checked
   ```
3. Nhấp **Test Kết nối**

**Ví dụ cho các mail server phổ biến:**

| Mail Server | Host                  | Port   | TLS |
| ----------- | --------------------- | ------ | --- |
| Gmail       | smtp.gmail.com        | 587    | ✓   |
| Outlook     | smtp-mail.outlook.com | 587    | ✓   |
| Yahoo       | smtp.mail.yahoo.com   | 587    | ✓   |
| Company     | mail.company.com      | 587-25 | ✓   |

### 3. SendGrid

#### 3.1 Tạo SendGrid Account

1. Truy cập: https://sendgrid.com/
2. Đăng ký tài khoản mới
3. Xác nhận email

#### 3.2 Lấy API Key

1. Vào: **Settings** → **API Keys**
2. Nhấp **Create API Key**
3. Đặt tên: `Accounting Notifications`
4. Copy API Key

#### 3.3 Cấu hình trong Odoo

1. Vào: **Accounting** → **Cấu hình Thông báo** → **Email**
2. Tạo cấu hình mới:
   ```
   Tên: SendGrid Production
   Nhà cung cấp Email: SendGrid API
   SendGrid Sender Email: noreply@company.com
   SendGrid API Key: [Dán API Key]
   ```
3. Nhấp **Test Kết nối**

---

## Cấu hình SMS

### 1. Viettel SMS API (Khuyến nghị cho Việt Nam)

#### 1.1 Liên hệ Viettel

- **Bộ phận**: Viettel Telecom - SMS Service
- **Yêu cầu**: API để gửi SMS thông báo
- **Thông tin cần**:
  - Company/Organization name
  - Số điện thoại liên hệ
  - Mục đích sử dụng (Notification Service)

#### 1.2 Nhận thông tin từ Viettel

Viettel sẽ cung cấp:

- CP Code (Customer Portal Code)
- API URL
- Username & Password

#### 1.3 Cấu hình trong Odoo

1. Vào: **Accounting** → **Cấu hình Thông báo** → **SMS**
2. Tạo cấu hình mới:
   ```
   Tên: Viettel Production
   Nhà cung cấp SMS: Viettel SMS API
   Viettel CP Code: [Từ Viettel]
   Username: [Từ Viettel]
   Password: [Từ Viettel]
   Sender ID: SYSTEM (Sẽ hiển thị trên điện thoại)
   API URL: https://api.viettel.com.vn/sms/send (hoặc URL từ Viettel)
   ```
3. Nhấp **Test Kết nối**

### 2. Twilio

#### 2.1 Tạo Twilio Account

1. Truy cập: https://www.twilio.com/
2. Đăng ký tài khoản mới
3. Xác nhận số điện thoại

#### 2.2 Lấy Credentials

1. Vào: **Console** → **Account**
2. Lấy **Account SID**
3. Lấy **Auth Token**
4. Mua số SMS: **Messaging** → **Phone Numbers** → **Buy a Number**
5. Chọn số điện thoại (ví dụ: +1234567890)

#### 2.3 Cấu hình trong Odoo

1. Vào: **Accounting** → **Cấu hình Thông báo** → **SMS**
2. Tạo cấu hình mới:
   ```
   Tên: Twilio Production
   Nhà cung cấp SMS: Twilio
   Twilio Account SID: [Từ Twilio]
   Twilio Auth Token: [Từ Twilio]
   Twilio Phone Number: +1234567890
   ```
3. Nhấp **Test Kết nối**

### 3. AWS SNS

#### 3.1 Tạo AWS Account

1. Truy cập: https://aws.amazon.com/
2. Tạo tài khoản
3. Truy cập **AWS Console**

#### 3.2 Tạo IAM User

1. **IAM** → **Users** → **Create user**
2. Đặt tên: `accounting-notifications`
3. **Attach policies**:
   - `AmazonSNSFullAccess`
4. Tạo **Access Key**
5. Copy:
   - Access Key ID
   - Secret Access Key

#### 3.3 Cấu hình trong Odoo

1. Vào: **Accounting** → **Cấu hình Thông báo** → **SMS**
2. Tạo cấu hình mới:
   ```
   Tên: AWS SNS Production
   Nhà cung cấp SMS: AWS SNS
   AWS Access Key: [Copy từ IAM]
   AWS Secret Key: [Copy từ IAM]
   AWS Region: ap-southeast-1 (hoặc region khác)
   ```
3. Nhấp **Test Kết nối**

---

## Cấu hình Thông báo

### Loại Thông báo

#### 1. Khấu hao Định kỳ Hoàn thành 📊

**Khi nào gửi:**

- Chạy lịch khấu hao định kỳ
- Khấu hao thực hiện thành công

**Nội dung:**

```
Tiêu đề: Khấu hao tài sản: [Tên tài sản]
Nội dung:
- Tên tài sản: [Asset name]
- Giá trị khấu hao: [Amount]
- Phương pháp: [Method]
- Số kỳ còn lại: [Periods left]
```

#### 2. Phát hiện Bất thường 🚨

**Khi nào gửi:**

- AI phát hiện bất thường trong dữ liệu tài sản

**Nội dung:**

```
Tiêu đề: ⚠️ Phát hiện bất thường: [Tên tài sản]
Nội dung:
- Loại bất thường: [Anomaly type]
- Mô tả: [Description]
- Mức độ: [Severity: High/Medium/Low]
- Khuyến nghị: [AI Recommendation]
```

#### 3. Tài sản Sắp Hết Hạn ⏰

**Khi nào gửi:**

- Tài sản sắp hết thời gian sử dụng (trong 30 ngày)

**Nội dung:**

```
Tiêu đề: Tài sản sắp hết niên hạn: [Tên tài sản]
Nội dung:
- Tên tài sản: [Asset name]
- Ngày hết hạn: [Expiration date]
- Còn lại: [Days remaining]
- Khuyến nghị: Cân nhắc thanh lý hoặc tái đầu tư
```

### Cấu hình Người nhận

**Email:**

- Cấu hình trong **Asset** hoặc **User**:
  - Email address: người@company.com
  - Enable notifications: ✓

**SMS:**

- Cấu hình trong **User** hoặc **Department**:
  - Phone number: +84912345678
  - Enable SMS: ✓

---

## Sử dụng Thực tế

### 1. Kiểm tra Nhật ký Thông báo

1. Vào: **Accounting** → **Nhật ký Thông báo**
2. Xem trạng thái:
   - ✅ **Sent** - Đã gửi thành công
   - ⏳ **Pending** - Chờ gửi
   - ❌ **Failed** - Lỗi gửi

### 2. Thử lại Thông báo Lỗi

1. Chọn thông báo có trạng thái **Failed**
2. Nhấp **Thử lại**
3. Kiểm tra lại

### 3. Tìm kiếm Thông báo

- Lọc theo: Loại sự kiện, trạng thái, người nhận
- Nhóm theo: Trạng thái, ngày, loại sự kiện

---

## Xử lý Lỗi Thường gặp

### Email Errors

**"Gmail Service Account JSON không hợp lệ"**

```
📌 Kiểm tra:
- JSON file từ Google Cloud Console đầy đủ đoạn
- Dán toàn bộ nội dung (không chỉ phần nào)
- Kiểm tra không có khoảng trắng dư thừa
```

**"SMTP Connection Refused"**

```
📌 Kiểm tra:
- SMTP Host & Port chính xác
- Tài khoản & mật khẩu đúng
- Firewall cho phép SMTP port
- Kết nối Internet bình thường
```

**"SendGrid API Key Invalid"**

```
📌 Kiểm tra:
- API Key còn hạn sử dụng (Settings → API Keys)
- Prefixes của API Key phù hợp (Full Access recommended)
- Copy đầy đủ không cắt xén
```

### SMS Errors

**"Viettel API Connection Failed"**

```
📌 Kiểm tra:
- CP Code, Username, Password từ Viettel
- API URL đúng (hỏi lại Viettel nếu cần)
- Kết nối Internet ổn định
- Số điện thoại nhận có đúng định dạng (08xxxxxxxx hoặc +84912345678)
```

**"Twilio Auth Failed"**

```
📌 Kiểm tra:
- Account SID từ Console
- Auth Token from console.twilio.com
- Không copy sai số 0 thành O chữ
- Account vẫn còn credit
```

**"AWS SNS Permission Denied"**

```
📌 Kiểm tra:
- IAM User có quyền SNS
- Access Key & Secret Key chính xác
- Region đúng (ap-southeast-1 cho Việt Nam)
- Phone number có định dạng: +84912345678
```

---

## Chi phí Ước tính

### Email

| Provider | Chi phí                          |
| -------- | -------------------------------- |
| Gmail    | Miễn phí\*                       |
| SMTP     | Căn cứ Server                    |
| SendGrid | $14-300/tháng (100K-500K emails) |

\*Gmail: Miễn phí với Limited use access. Nếu lượng email lớn, cần upgrade API quota

### SMS

| Provider | Chi phí                                 |
| -------- | --------------------------------------- |
| Viettel  | ~1,000-2,000 VND/SMS (tuỳ package)      |
| Twilio   | ~$0.0075/SMS (US), ~$0.10-0.15/SMS (VN) |
| AWS SNS  | ~$0.0645/SMS (tuỳ region)               |

**Khuyến nghị**: Sử dụng **Viettel SMS** cho chi phí thấp ở Việt Nam

---

## Bảo mật

### Best Practices

1. **API Keys/Credentials**
   - ✅ Lưu trong Odoo (encrypted field)
   - ❌ KHÔNG lưu trong source code
   - ❌ KHÔNG commit vào Git
   - ❌ KHÔNG chia sẻ công khai

2. **Permissions**
   - Gmail/SendGrid: Chỉ cấp quyền "Send"
   - SMS: Chỉ cấp quyền "Send SMS"
   - IAM: Chỉ cấp quyền cần thiết

3. **Rate Limiting**
   - Không gửi quá nhiều email/SMS cùng lúc
   - Cấu hình số lần thử lại hợp lý (default: 3)
   - Để nguyên thời gian chờ giữa các lần gửi

4. **Monitoring**
   - Kiểm tra **Nhật ký Thông báo** hàng ngày
   - Alert nếu tỷ lệ thất bại cao
   - Review failed messages để fix root cause

---

## Tích hợp với Automated Jobs

### Kích hoạt Thông báo Tự động

**Khấu hao Định kỳ:**

```python
# Trong asset_depreciation_schedule.py
def action_run_depreciation(self):
    # ... chạy khấu hao ...

    # Gửi thông báo
    notification_log = self.env['notification.log'].create_log(
        subject=f'Khấu hao: {self.asset_id.name}',
        event_type='depreciation_completed',
        notification_type='email_sms',
        email_to='manager@company.com',
        sms_to='+84912345678'
    )
    self.env['notification.service'].send_notification(notification_log)
```

**Phát hiện Bất thường:**

```python
# Trong asset_ai_analysis.py
def _analyze_with_gemini(self):
    # ... phân tích AI ...

    if anomalies_found:
        notification_log = self.env['notification.log'].create_log(
            subject=f'Phát hiện bất thường: {self.asset_id.name}',
            event_type='anomaly_detected',
            notification_type='sms'
        )
```

---

## Hỗ trợ & Liên hệ

**Gặp vấn đề?**

1. Kiểm tra **Nhật ký Thông báo** > chi tiết lỗi
2. Xem phần **Xử lý Lỗi** phía trên
3. Thử lại **Test Kết nối**
4. Liên hệ IT support nếu cần

**Cần mở rộng?**

- Thêm provider email khác: Edit `notification_service.py`
- Thêm SMS provider: Edit `notify_sms_config.py` + `notification_service.py`
- Thêm event type: Edit `notification_log.py` + workflows

---

**Phiên bản**: 1.0  
**Cập nhật**: 2024  
**Module**: Accounting Module 1.0  
**External APIs**: Gmail, SMTP, SendGrid, Viettel, Twilio, AWS SNS
