# Hướng dẫn Cấu hình Google Gemini AI

## Tổng quan

Module Accounting đã được tích hợp với Google Gemini API để cung cấp khả năng phân tích AI nâng cao cho:

- Phân tích tài sản và khấu hao
- Phát hiện bất thường trong dữ liệu kế toán
- Gợi ý cải thiện quản lý tài sản

## Yêu cầu

- **Python 3.8+**
- **Odoo 15.0+**
- **google-generativeai>=0.3.0** (sẽ được cài đặt tự động)

## Bước 1: Lấy API Key từ Google Gemini

### 1.1 Truy cập Google AI Studio

- Mở trình duyệt và truy cập: https://aistudio.google.com/
- Đăng nhập bằng tài khoản Google của bạn

### 1.2 Tạo hoặc lấy API Key

- Nhấp vào **"Get API Key"** hoặc truy cập: https://aistudio.google.com/app/apikeys
- Chọn **"Create API Key"** nếu chưa có
- Copy API Key (nó sẽ có dạng: `AIzaSy...`)

### 1.3 Bảo mật API Key

⚠️ **QUAN TRỌNG**:

- Không chia sẻ API Key với bất kỳ ai
- Không commit API Key vào Git
- dùng API Key trong code
- Sử dụng biến môi trường hoặc cấu hình trong Odoo

## Bước 2: Cấu hình trong Odoo

### 2.1 Kích hoạt Module

1. Vào: **Addons** → **Apps**
2. Tìm kiếm: `Accounting Module` (Accounting)
3. Nhấp **Install**

### 2.2 Cấu hình Google Gemini

1. Vào: **Accounting** → **Configuration** → **Cấu hình AI**
2. Nhấp **Create** để tạo cấu hình mới
3. Điền các thông tin:

```
Tên Cấu hình: Google Gemini Production
API Key Google Gemini: [Dán API Key ở đây]
Mô hình: gemini-1.5-pro (hoặc gemini-1.5-flash)
Ngôn ngữ: Vietnamese
Nhiệt độ: 0.7
Max Tokens: 2000
```

### 2.3 Kiểm tra Kết nối

1. Trong form cấu hình, nhấp nút **"Test Kết nối"**
2. Chờ kết quả:
   - ✅ **Success**: Kết nối thành công
   - ❌ **Error**: Kiểm tra lại API Key hoặc kết nối mạng

## Bước 3: Sử dụng Gemini AI

### 3.1 Phân tích Tài sản

1. Vào **Accounting** → **Assets** (Tài sản)
2. Mở một tài sản
3. Nhấp **Analyze with AI** (Phân tích bằng AI)
4. Chọn **Gemini Analysis**
5. Xem kết quả phân tích:
   - **Analysis**: Phân tích chi tiết
   - **Recommendations**: Khuyến nghị
   - **Anomalies**: Bất thường phát hiện

### 3.2 Phân tích Định kỳ

- AI tự động phân tích tài sản theo lịch trình
- Kết quả được lưu dưới dạng log
- Cảnh báo được gửi nếu phát hiện bất thường

## Các Mô hình Gemini Có sẵn

| Mô hình              | Ưu điểm                          | Nhược điểm        |
| -------------------- | -------------------------------- | ----------------- |
| **gemini-1.5-pro**   | Chính xác cao, hiểu ngữ cảnh tốt | Chi phí cao hơn   |
| **gemini-1.5-flash** | Nhanh, chi phí thấp              | Chính xác hơi kém |
| **gemini-pro**       | Sẵn sàng (legacy)                | Kém chính xác hơn |

**Khuyến nghị**: Dùng `gemini-1.5-pro` cho phân tích tài chính, `gemini-1.5-flash` cho phân tích nhanh.

## Các Tham số Cấu hình

### Temperature (Nhiệt độ)

- **0.0**: Luôn luôn lặp lại câu trả lời (xác định)
- **0.5**: Cân bằng (khuyến nghị)
- **0.7 - 0.9**: Creative, đa dạng hơn
- **1.0**: Hoàn toàn random

**Khuyến nghị**: 0.5 - 0.7 cho phân tích tài chính

### Max Tokens

- **1000**: Đủ cho phân tích ngắn
- **2000 - 4000**: Chi tiết hơn (khuyến nghị)
- **>4000**: Cho phân tích rất chi tiết

## Xử lý Lỗi

### 1. "Lỗi: API Key không hợp lệ"

```
Giải pháp:
- Kiểm tra lại API Key (không có khoảng trắng đầu/cuối)
- Đảm bảo API Key chưa bị vô hiệu hóa
- Kiểm tra tại https://aistudio.google.com/app/apikeys
```

### 2. "Lỗi: Kết nối bị từ chối"

```
Giải pháp:
- Kiểm tra kết nối Internet
- Kiểm tra tường lửa (firewall) không chặn Google API
- Thử lại sau vài giây
```

### 3. "Lỗi: Vượt quá giới hạn yêu cầu"

```
Giải pháp:
- Đợi vài phút rồi thử lại
- Nâng cấp tài khoản Google Cloud nếu cần
- Giảm tần suất phân tích tự động
```

### 4. "Rơi về phân tích cục bộ (Local Analysis)"

```
Giải pháp:
- Kiểm tra log Odoo (Warning level)
- Đảm bảo google-generativeai được cài đặt
- Nếu OK: Fallback an toàn, không ảnh hưởng chức năng
```

## Giám sát và Bảo trì

### Kiểm tra Trạng thái

1. Vào: **Accounting** → **Configuration** → **Cấu hình AI**
2. Xem cột:
   - **Is Configured**: Đã cấu hình chưa?
   - **Test Status**: Trạng thái kết nối cuối cùng
   - **Last Test**: Lần test cuối

### Xem Log Phân tích

1. Vào: **Accounting** → **AI Analysis**
2. Lọc theo:
   - Asset
   - Thời gian
   - Trạng thái (success/error)

### Cập nhật API Key

1. Mở cấu hình Gemini
2. Chỉnh sửa trường **API Key**
3. Nhấp **Save** rồi **Test Kết nối**

## Chi phí sử dụng

### Giá Gemini API (tính theo input/output tokens)

- **gemini-1.5-pro**:
  - Input: $1.25 per 1M tokens
  - Output: $5.00 per 1M tokens

- **gemini-1.5-flash**:
  - Input: $0.075 per 1M tokens
  - Output: $0.30 per 1M tokens

### Ước tính

- Phân tích 1 tài sản: ~500-1000 tokens (~$0.005)
- 100 phân tích/tháng: ~$0.50
- 1000 phân tích/tháng: ~$5.00

**Lưu ý**: Google cấp free tier ~$300/tháng cho tài khoản mới

## Tính năng Gemini AI trong Module

### Phân tích Tài sản 🔍

```
Input:
- Giá trị gốc, giá trị hiện tại
- Thời gian sử dụng
- Tình trạng
- Lịch sử khấu hao

Output:
- Đánh giá giá trị còn lại
- Khuyến nghị thay thế
- Phát hiện bất thường
- Tối ưu hóa khấu hao
```

### Phát hiện Bất thường 🚨

```
Gemini phát hiện:
- Giá trị giảm bất thường
- Mô hình khấu hao lạ
- Vô lý về thời gian sử dụng
- Chênh lệch kế toán
```

### Gợi ý Cải thiện 💡

```
Khuyến nghị:
- Tối ưu hóa phương pháp khấu hao
- Kế hoạch bảo trì/thay thế
- Cấp bổ sung hoặc thanh lý
- Điều chỉnh chính sách khấu hao
```

## Tính Năng Fallback ⚙️

Nếu Gemini API không khả dụng:

- ✅ Module tự động rơi về phân tích cục bộ
- ✅ Không gây gián đoạn chức năng
- ✅ Hệ thống tự động toàn bộ

```
Luồng:
1. Cố gắng kết nối Gemini
   ↓
2. Nếu lỗi → Rơi về phân tích local
   ↓
3. Ghi log warning
   ↓
4. Tiếp tục xử lý bình thường
```

## Hỗ trợ Ngôn ngữ

Module hỗ trợ AI phân tích bằng các ngôn ngữ:

- 🇻🇳 **Vietnamese** (Khuyến nghị)
- 🇬🇧 **English**
- 🇬🇧 **Auto-detect** (Tự động)

**Khuyến nghị**: Chọn **Vietnamese** để kết quả phù hợp nhất với dữ liệu Việt Nam

## Câu hỏi Thường gặp (FAQ)

**Q: Có mất phí nếu sử dụng Gemini không?**
A: Có, nhưng rất thấp (~$0.005/phân tích). Google cấp $300 free tier.

**Q: Dữ liệu của tôi có được chia sẻ với Google không?**
A: Chỉ dữ liệu cần thiết để phân tích mới được gửi. Google AI Studio tuân thủ GDPR.

**Q: Có thể sử dụng API Key khác không?**
A: Có, cấu hình trong **Cấu hình AI** rồi nhấp **Save**.

**Q: Tại sao phân tích có khi chậm?**
A: Phụ thuộc vào:

- Tốc độ Internet
- Độ phức tạp dữ liệu
- Tải của Gemini API

**Q: Module có thể chạy mà không có Gemini không?**
A: Có! Fallback tự động dùng phân tích local.

## Liên hệ Hỗ trợ

Gặp vấn đề? Vui lòng:

1. Kiểm tra lại các bước setup
2. Xem log (Accounting → AI Analysis)
3. Thử test kết nối lại
4. Liên hệ team IT

---

**Phiên bản**: 1.0  
**Cập nhật**: 2024  
**Module**: Accounting Module 1.0  
**Odoo**: 15.0+
