# -*- coding: utf-8 -*-
{
    'name': "Trang Chủ HNDN",
    'summary': "Bảng điều khiển tổng quan cho hệ thống HNDN",
    'version': '1.0',
    'category': 'Extra Tools',
    'author': "Antigravity",
    'depends': ['base', 'nhan_su', 'quan_ly_tai_chinh', 'quan_ly_tai_san'],
    'data': [
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'q_trang_chu/static/src/css/dashboard.css',
            'q_trang_chu/static/src/css/premium_ui.css',
            'q_trang_chu/static/src/js/dashboard_component.js',
        ],
        'web.assets_qweb': [
            'q_trang_chu/static/src/xml/dashboard_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
}
