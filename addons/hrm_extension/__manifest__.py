# -*- coding: utf-8 -*-
{
    'name': "HRM Extension",
    'summary': """Mở rộng chức năng HR - Quản lý nhân viên và tài sản""",
    'description': """
        Mở rộng module HR với:
        - Gán tài sản cho nhân viên
        - Lịch sử tài sản của nhân viên
        - Báo cáo tài sản theo nhân viên
    """,
    'author': "TTDN Team",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '1.0',
    'depends': ['base', 'nhan_su', 'quan_ly_tai_san', 'accounting_module'],
    'data': [
        'security/ir.model.access.csv',
        'views/nhan_vien_extension_view.xml',
        'views/asset_assignment_view.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
