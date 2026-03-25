# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AutomationRules(models.Model):
    """Quy tắc tự động hóa"""
    _name = 'automation.rules'
    _description = 'Automation Rules'

    name = fields.Char('Tên quy tắc')
    is_active = fields.Boolean('Kích hoạt', default=True)

    @api.model
    def apply_rules(self):
        """Áp dụng các quy tắc tự động"""
        pass
