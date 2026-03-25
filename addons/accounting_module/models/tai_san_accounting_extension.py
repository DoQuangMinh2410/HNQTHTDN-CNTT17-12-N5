# -*- coding: utf-8 -*-
from odoo import models, fields


class TaiSanAccountingExtension(models.Model):
    _inherit = 'tai_san'

    depreciation_ids = fields.One2many(
        'asset.depreciation',
        'asset_id',
        string='Danh sách Khấu hao'
    )
    depreciation_schedule_id = fields.Many2one(
        'asset.depreciation.schedule',
        string='Lịch khấu hao'
    )
    account_move_ids = fields.One2many(
        'account.move.custom',
        'asset_id',
        string='Bút toán kế toán'
    )

    def action_confirm(self):
        res = super().action_confirm()
        for record in self:
            if record.pp_khau_hao != 'none' and record.usage_status == 'in_use':
                schedule = record.depreciation_schedule_id
                if not schedule:
                    schedule = self.env['asset.depreciation.schedule'].create({
                        'asset_id': record.id,
                        'original_value': record.gia_tri_ban_dau,
                        'depreciation_method': 'straight_line' if record.pp_khau_hao == 'straight-line' else 'degressive',
                        'useful_life_months': record.thoi_gian_toi_da * 12,
                        'annual_rate': record.ty_le_khau_hao,
                        'start_date': fields.Date.today(),
                    })
                    record.depreciation_schedule_id = schedule.id
                schedule.action_generate_depreciation()
        return res
