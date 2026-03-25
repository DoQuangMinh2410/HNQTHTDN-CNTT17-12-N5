# 🛠️ TECHNICAL DOCUMENTATION - Odoo 15 Asset System

## 📁 Project Structure

```
addons/
├── nhan_su/                          # HR Module (existing)
│   ├── models/
│   │   ├── nhan_vien.py             # Employee model
│   │   ├── phong_ban.py             # Department model
│   │   ├── chuc_vu.py               # Job position model
│   │   └── lich_su_cong_tac.py      # Work history model
│   └── ...
│
├── quan_ly_tai_san/                  # Asset Management Module (extended)
│   ├── models/
│   │   ├── tai_san.py               # Asset model
│   │   ├── tai_san_extension.py      # Asset extension (NEW)
│   │   ├── danh_muc_tai_san.py      # Asset category
│   │   ├── phan_bo_tai_san.py       # Asset distribution
│   │   ├── lich_su_khau_hao.py      # Depreciation history
│   │   ├── automation_rules.py       # Automation rules (NEW)
│   │   └── ...
│   └── ...
│
├── hrm_extension/                    # HR Extension Module (NEW)
│   ├── models/
│   │   └── asset_assignment.py      # Asset assignment to employee
│   ├── views/
│   │   ├── asset_assignment_view.xml
│   │   ├── nhan_vien_extension_view.xml
│   │   └── menu.xml
│   ├── security/
│   │   └── ir.model.access.csv
│   └── __manifest__.py
│
└── accounting_module/                # Accounting Module (NEW)
    ├── models/
    │   ├── asset_depreciation.py     # Depreciation records
    │   ├── account_move.py           # Accounting entries
    │   ├── asset_depreciation_schedule.py  # Depreciation schedule
    │   └── asset_ai_analysis.py      # AI analysis
    ├── views/
    │   ├── asset_depreciation_view.xml
    │   ├── account_move_view.xml
    │   ├── asset_ai_analysis_view.xml
    │   └── menu.xml
    ├── security/
    │   └── ir.model.access.csv
    ├── report/
    │   └── depreciation_report.xml
    ├── data/
    │   └── scheduled_jobs.xml
    ├── demo/
    │   └── demo_data.xml
    └── __manifest__.py
```

## 🔄 Data Flow

### 1. Employee Creation (HR Module)

```python
Model: nhan_vien
Fields:
  - ma_dinh_danh (ID)
  - ho_ten (Name)
  - ngay_sinh (DOB)
  - email, so_dien_thoai (Contact)
```

### 2. Asset Creation (Asset Management)

```python
Model: tai_san
Fields:
  - ma_tai_san (Asset Code)
  - ten_tai_san (Asset Name)
  - ngay_mua_ts (Purchase Date)
  - gia_tri_ban_dau (Initial Value)
  - danh_muc_ts_id (Category)
  - pp_khau_hao (Depreciation Method)
  - thoi_gian_toi_da (Useful Life)
  - phan_bo_employee_id (Assigned Employee) ← NEW
  - assignment_date ← NEW
  - usage_status ← NEW
  - depreciation_schedule_id ← NEW
  - depreciation_ids ← NEW (One2many)
  - account_move_ids ← NEW (One2many)
```

### 3. Asset Confirmation

```python
# Trigger: action_confirm() method
Asset.usage_status: draft → in_use

Operations:
  1. Create AssetDepreciationSchedule
  2. Generate AssetDepreciation records (monthly)
  3. Create initial AccountMove entries
```

### 4. Depreciation Calculation

```python
Model: asset.depreciation.schedule
Formula (Straight-line):
  monthly_depreciation = original_value / useful_life_months

Formula (Degressive):
  monthly_depreciation = remaining_value × (annual_rate / 100 / 12)
```

### 5. Accounting Entry

```python
Model: account.move.custom
Fields:
  - asset_id (FK: tai_san)
  - employee_id (FK: nhan_vien)
  - amount (Depreciation amount)
  - date (Entry date)
  - move_type (depreciation/disposal/adjustment)
  - state (draft/posted)

Auto-created when:
  - AssetDepreciation is confirmed
  - status = 'posted'
```

### 6. AI Analysis

```python
Model: asset.ai.analysis
Method: _perform_local_analysis()
Returns:
  - Analysis text (statistics)
  - Recommendations (optimization tips)
  - Anomalies (alerts)
```

## 🔧 Key Implementation Details

### 1. Inheritance Pattern

#### Asset Extension (quan_ly_tai_san)

```python
# tai_san_extension.py
_inherit = 'tai_san'

# New fields
phan_bo_employee_id
depreciation_ids (One2many)
depreciation_schedule_id
account_move_ids
usage_status

# New methods
action_confirm()
action_assign_employee()
schedule_monthly_depreciation() [Cron]
```

### 2. Scheduled Job (Cron)

```xml
<!-- data/scheduled_jobs.xml -->
<record id="ir_cron_monthly_depreciation" model="ir.cron">
    <field name="name">Generate Monthly Depreciation</field>
    <field name="model_id" ref="accounting_module.model_asset_depreciation_schedule"/>
    <field name="code">env['tai_san'].schedule_monthly_depreciation()</field>
    <field name="interval_type">months</field>
    <field name="interval_number">1</field>
</record>

Execution:
  - Runs: 1st of every month (default)
  - Task: Check for missing depreciation, create if needed
  - Silent: No user interaction required
```

### 3. Automation Workflow

```python
# When asset status changes:
asset.write({'usage_status': 'in_use'})
  ↓
@api.onchange triggered
  ↓
action_confirm() called
  ↓
Create depreciation schedule & records
  ↓
Create initial accounting entries
  ↓
Cron job runs monthly to create new records
```

### 4. Permission Model

```csv
# security/ir.model.access.csv

# For Users
access_asset_depreciation_user,1,1,1,1
  → Read, Write, Create, Unlink

# For Managers (System group)
access_asset_depreciation_manager,1,1,1,1
  → All permissions
```

## 📊 Models Relationships

```
nhan_vien (1)
    ↓
    ├─→ asset.assignment (M) ← tai_san (1)
    │
    ├─→ tai_san (M) [via phan_bo_employee_id]
    │
    └─→ asset.depreciation (M) [via employee_id]
            ↓
            account.move.custom (1) [account_move_id]
```

## 🎯 API Endpoints & Methods

### Asset Operations

```python
asset.action_confirm()
  # Confirm asset & generate depreciation

asset.action_assign_employee()
  # Assign employee to asset

asset.action_depreciate()
  # Create depreciation immediately

asset.schedule_monthly_depreciation()
  # [Cron Job] Monthly depreciation generator
```

### Depreciation Operations

```python
depreciation.action_confirm()
  # Confirm depreciation & create accounting entry

depreciation.action_post()
  # Post depreciation (mark as posted)

depreciation._create_account_move()
  # Auto-create accounting entry
```

### AI Analysis

```python
analysis.action_analyze()
  # Run analysis & generate report

analysis.action_export_report()
  # Send report via email

analysis._perform_local_analysis(assets)
  # Local analysis without external API
```

## 📧 Email Integration

### Configuration

```
Admin → Settings → Technical → Email Configuration
  - SMTP Server: smtp.gmail.com
  - SMTP Port: 587
  - SMTP User: your-email@gmail.com
  - Security: TLS
```

### Email Sending

```python
# In asset_ai_analysis.py

mail = self.env['mail.mail'].create({
    'subject': 'Asset Analysis Report',
    'body_html': html_content,
    'email_to': user.email,
})
mail.send()
```

## 🗄️ Database Schema

### Tables

```sql
-- Core tables
CREATE TABLE nhan_vien (
    id INTEGER PRIMARY KEY,
    ma_dinh_danh VARCHAR(50) UNIQUE,
    ho_ten VARCHAR(255),
    ngay_sinh DATE,
    email VARCHAR(255),
    so_dien_thoai VARCHAR(20)
);

CREATE TABLE tai_san (
    id INTEGER PRIMARY KEY,
    ma_tai_san VARCHAR(50) UNIQUE,
    ten_tai_san VARCHAR(255),
    ngay_mua_ts DATE,
    gia_tri_ban_dau FLOAT,
    gia_tri_hien_tai FLOAT,
    pp_khau_hao VARCHAR(20),
    phan_bo_employee_id INTEGER REFERENCES nhan_vien(id),
    usage_status VARCHAR(20),
    depreciation_schedule_id INTEGER
);

CREATE TABLE asset_depreciation (
    id INTEGER PRIMARY KEY,
    asset_id INTEGER REFERENCES tai_san(id),
    employee_id INTEGER REFERENCES nhan_vien(id),
    date DATE,
    depreciation_amount FLOAT,
    remaining_value FLOAT,
    state VARCHAR(20)
);

CREATE TABLE account_move_custom (
    id INTEGER PRIMARY KEY,
    asset_id INTEGER REFERENCES tai_san(id),
    employee_id INTEGER REFERENCES nhan_vien(id),
    amount FLOAT,
    date DATE,
    move_type VARCHAR(20),
    state VARCHAR(20)
);
```

## 🧪 Testing Checklist

```
[ ] 1. Create employee
[ ] 2. Create asset with employee assignment
[ ] 3. Confirm asset (triggers depreciation creation)
[ ] 4. Verify depreciation records created (60 months)
[ ] 5. Confirm first depreciation
[ ] 6. Verify accounting entry created
[ ] 7. Run AI analysis
[ ] 8. Send report email
[ ] 9. Check asset in employee record
[ ] 10. Return asset (mark_damaged / return_asset)
```

## 🚀 Deployment

### Step 1: Install Modules

```bash
# Via Odoo UI
Apps → Search → accounting_module → Install
Apps → Search → hrm_extension → Install
```

### Step 2: Load Demo Data

```
During installation, select "Load Demo Data"
or manually load via:
  Admin → Load Demo Data
```

### Step 3: Configure

```
Settings → Email Configuration (SMTP)
Settings → Scheduled Actions (verify cron)
```

### Step 4: Test

```
Follow Testing Checklist above
```

## 📝 Code Examples

### Create Asset

```python
asset = env['tai_san'].create({
    'ma_tai_san': 'TS001',
    'ten_tai_san': 'Laptop Dell',
    'ngay_mua_ts': date.today(),
    'gia_tri_ban_dau': 25000000,
    'gia_tri_hien_tai': 25000000,
    'pp_khau_hao': 'straight-line',
    'thoi_gian_toi_da': 5,
    'phan_bo_employee_id': employee.id,
    'usage_status': 'draft',
})

# Confirm asset
asset.action_confirm()
# ↓
# Depreciation schedule created
# Depreciation records created (60 months)
```

### Query Depreciation

```python
depreciation_records = env['asset.depreciation'].search([
    ('asset_id', '=', asset.id),
    ('state', '=', 'posted'),
])

total_depreciated = sum(d.depreciation_amount for d in depreciation_records)
```

### Run Analysis

```python
analysis = env['asset.ai.analysis'].create({
    'analysis_date': date.today(),
})
analysis.action_analyze()
```

## 🐛 Common Issues & Solutions

### Issue: Depreciation not created

**Solution:**

1. Check asset status = 'in_use'
2. Verify depreciation_method ≠ 'none'
3. Run cron manually
4. Check logs for errors

### Issue: Email not sent

**Solution:**

1. Configure SMTP properly
2. Check email address is correct
3. Verify firewall allows SMTP
4. Check email client logs

### Issue: Accounting entry not posted

**Solution:**

1. Verify depreciation is confirmed
2. Check move_type = 'depreciation'
3. Manually trigger action_confirm()

## 📚 References

- Odoo 15 Documentation: https://docs.odoo.com/15.0/
- Models & Fields: https://docs.odoo.com/15.0/developer/reference/addons/models.html
- Views (XML): https://docs.odoo.com/15.0/developer/reference/addons/views.html
- Security: https://docs.odoo.com/15.0/developer/reference/addons/security.html
