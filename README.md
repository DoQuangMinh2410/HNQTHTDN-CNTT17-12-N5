# 🏢 Hệ Thống Quản Lý Tài Sản & Nhân Sự - Odoo 15

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Odoo](https://img.shields.io/badge/Odoo-15-green.svg)

---

## 📖 **Mục Lục**

1. [Giới thiệu dự án](#-giới-thiệu-dự-án)
2. [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
3. [Tải & Clone Project](#-tải--clone-project)
4. [Cài đặt Môi trường](#-cài-đặt-môi-trường)
5. [Cài đặt Thư viện](#-cài-đặt-thư-viện)
6. [Setup PostgreSQL](#-setup-postgresql)
7. [Cấu hình Odoo](#-cấu-hình-odoo)
8. [Chạy Hệ thống](#-chạy-hệ-thống)
9. [Demo Chức Năng](#-demo-chức-năng)
10. [Troubleshooting](#-troubleshooting)

---

## 🎯 **Giới Thiệu Dự Án**

**Hệ thống Quản Lý Tài Sản & Nhân Sự** là một giải pháp ERP tích hợp dựa trên **Odoo 15**, cung cấp các tính năng:

### 📌 **Các Module Chính:**

| Module | Chức Năng |
|--------|----------|
| **quan_ly_tai_san** | Quản lý toàn bộ tài sản, luân chuyển, mượn/trả, thanh lý |
| **nhan_su** | Quản lý nhân viên, phòng ban, chức vụ, lịch sử công tác |
| **accounting_module** | Khấu hao tài sản, ghi nhận kế toán, AI phân tích (Gemini), thông báo |
| **hrm_extension** | Mở rộng HR - gán tài sản cho nhân viên |
| **quan_ly_van_ban** | Quản lý văn bản đi/đến |

### ✨ **Tính Năng Nổi Bật:**

- ✅ **Dashboard** thống kê tài sản, luân chuyển, mượn/trả
- ✅ **Khấu hao tự động** theo năm sử dụng
- ✅ **Phân bổ tài sản** theo phòng ban
- ✅ **Kiểm kê tài sản** định kỳ
- ✅ **Quản lý mượn/trả** với trạng thái tự động
- ✅ **AI phân tích** với Google Gemini
- ✅ **Thông báo Email/SMS** khi có sự kiện
- ✅ **Báo cáo chi tiết** xuất PDF/Excel
- ✅ **Quản lý nhân viên** và gắn tài sản

---

## 💻 **Yêu Cầu Hệ Thống**

### **Phần Cứng:**
- RAM: ≥ 4GB (khuyến nghị 8GB)
- Disk: ≥ 20GB (để chứa database)
- CPU: 2+ cores

### **Phần Mềm:**
- **OS:** Linux (Ubuntu 20.04+) hoặc Windows (cài WSL2)
- **Python:** 3.8+
- **PostgreSQL:** 12+
- **Git:** Để clone project

---

## 📥 **Tải & Clone Project**

### **Bước 1: Mở Terminal/CMD**

```bash
# Tạo thư mục làm việc
mkdir ~/workspace
cd ~/workspace
```

### **Bước 2: Clone Project từ GitHub**

```bash
git clone https://github.com/[your-username]/odoo-asset-hr-management.git
cd odoo-asset-hr-management
```

**Hoặc:** Tải file ZIP từ GitHub → Giải nén

### **Bước 3: Kiểm tra cấu trúc**

```bash
ls -la
# Sẽ thấy: venv/, addons/, odoo/, odoo.conf, odoo-bin, requirements.txt, ...
```

---

## 🔧 **Cài đặt Môi trường**

### **Bước 1: Cài đặt các công cụ hệ thống (Ubuntu/Linux)**

```bash
sudo apt-get update
sudo apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-venv \
    libxml2-dev \
    libxslt-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    build-essential \
    libffi-dev \
    zlib1g-dev \
    libpq-dev \
    git \
    postgresql \
    postgresql-client
```

### **Bước 2: Tạo Virtual Environment**

```bash
# Tạo venv
python3 -m venv venv

# Kích hoạt venv (Linux/Mac)
source venv/bin/activate

# Hoặc kích hoạt venv (Windows - CMD)
# venv\Scripts\activate

# Hoặc kích hoạt venv (Windows - PowerShell)
# venv\Scripts\Activate.ps1
```

✅ Nếu thành công, Terminal sẽ thấy `(venv)` ở đầu dòng

### **Bước 3: Nâng cấp pip**

```bash
pip install --upgrade pip setuptools wheel
```

---

## 📦 **Cài đặt Thư viện**

### **Bước 1: Cài từ requirements.txt**

```bash
# Đảm bảo đã kích hoạt venv
source venv/bin/activate

# Cài đặt
pip install -r requirements.txt
```

**Thư viện chính bao gồm:**
- `odoo==15.0` - Framework ERP
- `psycopg2-binary` - Driver PostgreSQL
- `google-generativeai` - AI Gemini
- `requests` - HTTP client
- Và 50+ thư viện khác

### **Bước 2: Kiểm tra cài đặt**

```bash
python3 -c "import odoo; print(odoo.__version__)"
# Output: 15.0.1.0.0
```

---

## 🗄️ **Setup PostgreSQL**

### **Opción A: Cài PostgreSQL Trực Tiếp**

```bash
# Ubuntu/Debian
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Tạo user "odoo"
sudo -u postgres psql << EOF
CREATE USER odoo WITH PASSWORD 'odoo';
ALTER USER odoo CREATEDB;
ALTER USER odoo CREATEROLE;
\q
EOF

# Kiểm tra
psql -U odoo -h localhost -p 5432 -c "SELECT 1;"
```

### **Opción B: Dùng Docker (Tùy chọn)**

```bash
# Cài Docker & Docker Compose
sudo apt install docker.io docker-compose -y

# Tạo docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3'
services:
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
EOF

# Chạy
sudo docker-compose up -d
```

---

## ⚙️ **Cấu hình Odoo**

### **Bước 1: Tạo/Cập nhật odoo.conf**

File `odoo.conf` đã có sẵn. **Kiểm tra cấu hình:**

```bash
cat odoo.conf
```

**Cấu hình chuẩn:**

```ini
[options]
addons_path = addons
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = False
admin_passwd = admin
http_port = 8069
workers = 2
logfile = /tmp/odoo.log
log_level = info
```

**Giải thích:**
- `addons_path`: Đường dẫn module tùy chỉnh
- `db_host/port`: PostgreSQL server
- `db_user/password`: Credentials
- `admin_passwd`: Mật khẩu admin để tạo DB
- `http_port`: Cổng Odoo (8069)

### **Bước 2: Nếu cần sửa odoo.conf**

```bash
nano odoo.conf
# Hoặc dùng VS Code
code odoo.conf
```

---

## 🚀 **Chạy Hệ thống**

### **Lần Đầu Tiên (Khởi Tạo Database)**

```bash
# Kích hoạt venv
source venv/bin/activate

# Chạy với --init (tạo DB mới)
python3 odoo-bin -c odoo.conf -d odoo \
  --init=base,web,accounting_module,nhan_su,quan_ly_tai_san,quan_ly_van_ban,hrm_extension,website_forum
```

**Chờ tới khi thấy:**
```
[INFO] odoo.service.server: HTTP service (werkzeug) running on http://127.0.0.1:8069
```

### **Lần Sau (Chạy Bình Thường)**

```bash
# KHÔNG dùng --init (giữ database)
source venv/bin/activate
python3 odoo-bin -c odoo.conf
```

### **Mở Trình Duyệt**

```
http://localhost:8069
```

**Đăng nhập:**
- **Email:** admin
- **Mật khẩu:** admin

---

## 📊 **Demo Chức Năng**

### **1. Quản Lý Nhân Sự (nhan_su)**

Menu → **Nhân sự** → **Nhân viên**
- Tạo nhân viên
- Gán phòng ban, chức vụ
- Ghi lịch sử công tác

### **2. Quản Lý Tài Sản (quan_ly_tai_san)** - **CHÍNH**

Menu → **Quản lý tài sản**

**Tạo tài sản:**
```
Danh mục tài sản → Tạo: "Máy tính"
↓
Tài sản → Tạo: "Laptop Dell"
  - Loại: Máy tính
  - Giá: 50,000,000 VNĐ
  - Năm sử dụng: 5
  - Lưu → Tự động tính khấu hao!
```

**Luân chuyển:**
```
Luân chuyển tài sản → Tạo
  - Tài sản: Laptop Dell
  - Điểm chuyển: Phòng IT → Phòng HR
  - Lưu
```

**Mượn/Trả:**
```
Đơn mượn → Tạo: Nhân viên mượn laptop
Mượn/Trả → Tạo: Nhân viên trả laptop
```

### **3. Kế Toán (accounting_module)**

Menu → **Kế toán**
- Xem khấu hao tự động
- Ghi nhận bút toán
- Phân tích AI (Gemini)
- Báo cáo chi tiết

### **4. HR Extension**

Menu → **Nhân sự** → **Nhân viên** → Gắn tài sản

### **5. Diễn Đàn (website_forum)**

Menu → **Website** → **Diễn đàn**

---

## 🛠️ **Chạy Trong VS Code (Tuỳ chọn)**

### **Bước 1: Mở Workspace**

```bash
code /path/to/project
```

### **Bước 2: Mở Terminal (`Ctrl + ~`)**

### **Bước 3: Chạy**

```bash
source venv/bin/activate && python3 odoo-bin -c odoo.conf
```

### **Bước 4: Tạo Tasks (Tuỳ chọn)**

File `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start Odoo",
            "type": "shell",
            "command": "bash",
            "args": ["-c", "source venv/bin/activate && python3 odoo-bin -c odoo.conf"],
            "isBackground": true,
            "problemMatcher": {"pattern": {"regexp": ".*", "file": 1, "location": 2, "message": 3}}
        }
    ]
}
```

Rồi: **Terminal** → **Run Task** → **Start Odoo**

---

## 🐛 **Troubleshooting**

### **Lỗi 1: "connection refused" PostgreSQL**

```bash
# Khởi động PostgreSQL
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### **Lỗi 2: "password authentication failed"**

```bash
# Reset password
sudo -u postgres psql -c "ALTER USER odoo WITH PASSWORD 'odoo';"
```

### **Lỗi 3: "Port 8069 already in use"**

```bash
# Tìm process chiếm port
lsof -i :8069

# Kill process
kill -9 [PID]
```

### **Lỗi 4: Module không load**

```bash
# Update module
python3 odoo-bin -c odoo.conf -d odoo -u module_name

# Hoặc: Vào UI → Apps → Update
```

### **Lỗi 5: "Database not initialized"**

```bash
# Khởi tạo lại (LƯU Ý: xóa dữ liệu cũ!)
dropdb -U odoo -h localhost -p 5432 odoo
python3 odoo-bin -c odoo.conf -d odoo --init=base,web,accounting_module,...
```

---

## 📚 **Tài Liệu Thêm**

- [Odoo Documentation](https://www.odoo.com/documentation/15.0/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) - Chi tiết module
- [TECHNICAL_DOCUMENTATION.md](./TECHNICAL_DOCUMENTATION.md) - Kiến trúc

---

## 📞 **Liên Hệ & Hỗ Trợ**

- **Issues:** Mở issue trên GitHub
- **Email:** [your-email@example.com](mailto:your-email@example.com)
- **Docs:** Xem `/doc/` folder

---

## 📄 **License**

Dự án này được phát hành dưới giấy phép **AGPL-3.0**. Xem [LICENSE](./LICENSE) để biết chi tiết.

---

**Made with ❤️ by TTDN Team | Last Updated: March 2026**
    
