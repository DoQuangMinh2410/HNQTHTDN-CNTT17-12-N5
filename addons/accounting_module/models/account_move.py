# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime


class AccountMoveCustom(models.Model):
    _name = 'account.move.custom'
    _description = 'Bút toán kế toán'
    _rec_name = 'description'
    _order = 'date desc'

    asset_id = fields.Many2one('tai_san', string='Tài sản', ondelete='cascade')
    employee_id = fields.Many2one('nhan_vien', string='Nhân viên')
    
    amount = fields.Float('Số tiền', required=True)
    date = fields.Date('Ngày ghi nhận', required=True, default=fields.Date.today)
    
    description = fields.Char('Mô tả ghi nhận', required=True)
    
    move_type = fields.Selection([
        ('depreciation', 'Khấu hao'),
        ('disposal', 'Thanh lý'),
        ('adjustment', 'Điều chỉnh'),
    ], string='Loại ghi nhận', default='depreciation')
    
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('posted', 'Đã ghi sổ'),
    ], string='Trạng thái', default='draft')
    
    notes = fields.Text('Ghi chú')
    
    depreciation_id = fields.Many2one('asset.depreciation', string='Khấu hao liên quan')

    def action_post(self):
        """Ghi nhận bút toán"""
        self.state = 'posted'
        
    def action_draft(self):
        """Chuyển về nháp"""
        if self.state == 'posted':
            self.state = 'draft'

    @api.model
    def create(self, vals):
        """Override create để tư động ghi nhận nếu là khấu hao"""
        record = super().create(vals)
        if record.move_type == 'depreciation':
            record.state = 'posted'
        return record
