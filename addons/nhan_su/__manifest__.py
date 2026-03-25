# -*- coding: utf-8 -*-
{
    'name': "nhan_su",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'quan_ly_tai_chinh', 'hndn_ai_base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/nhan_vien.xml',
        'views/phong_ban.xml',
        'views/chuc_vu.xml',
        'views/lich_su_cong_tac.xml',
        'views/hop_dong.xml',
        'views/cham_cong.xml',
        'views/tinh_luong.xml',
        'views/phep_nam.xml',
        'views/khen_thuong_ky_luat.xml',
        'views/tam_ung.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {},
}
