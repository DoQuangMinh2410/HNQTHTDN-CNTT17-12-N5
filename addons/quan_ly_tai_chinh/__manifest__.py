# -*- coding: utf-8 -*-
{
    'name': "quan_ly_tai_chinh",

    'summary': """
        Đồng bộ Sổ cái Kế toán với Nhân sự và Tài sản
    """,

    'description': """
        Module quản lý tài chính kế toán nội bộ tự động hóa:
        - Hệ thống tài khoản
        - Sổ nhật ký / Bút toán
        - Chi tiết bút toán
    """,

    'author': "Tự Động Hóa Kế Toán",
    'category': 'Accounting/Accounting',
    'version': '0.1',

    # depends on base setup
    'depends': ['base', 'hndn_ai_base'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/tai_khoan_ke_toan.xml',
        'views/but_toan.xml',
        'views/bao_cao.xml',
        'views/menu.xml',
        'data/demo_tai_khoan.xml',
    ],
}
