# -*- coding: utf-8 -*-
{
    'name': "Accounting Module",
    'summary': """Quản lý Khấu hao và Kế toán tài sản""",
    'description': """
        Module quản lý khấu hao tài sản và ghi nhận các bút toán kế toán
        - Tính toán khấu hao tự động
        - Ghi nhận kế toán
        - Báo cáo khấu hao
        - Phân tích AI với Google Gemini
    """,
    'author': "TTDN Team",
    'website': "http://www.yourcompany.com",
    'category': 'Accounting',
    'version': '1.0',
    'license': 'AGPL-3',
    'depends': ['base', 'nhan_su', 'quan_ly_tai_san'],
    'external_dependencies': {
        'python': [
            'google-generativeai',
            'requests',
            'google-auth',
            'google-auth-httplib2',
            'google-auth-oauthlib',
            'google-api-python-client',
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/asset_depreciation_view.xml',
        'views/account_move_view.xml',
        'views/asset_ai_analysis_view.xml',
        'views/asset_gemini_config_view.xml',
        'views/notify_config_view.xml',
        'views/notification_log_view.xml',
        'report/depreciation_report.xml',
        'views/menu.xml',
        'data/scheduled_jobs.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'tests': [
        'tests/test_asset_depreciation_schedule.py',
    ],
    'installable': True,
    'auto_install': False,
}
