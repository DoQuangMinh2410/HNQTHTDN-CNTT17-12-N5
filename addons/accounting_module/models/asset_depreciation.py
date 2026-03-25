# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class AssetDepreciation(models.Model):
    _name = 'asset.depreciation'
    _description = 'Khấu hao tài sản'
    _rec_name = 'asset_id'
    _order = 'date desc'

    asset_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    employee_id = fields.Many2one('nhan_vien', string='Nhân viên được giao', related='asset_id.phan_bo_employee_id', store=True, readonly=False)
    date = fields.Date('Ngày khấu hao', required=True, default=fields.Date.today)
    month = fields.Char('Tháng', compute='_compute_month', store=True)
    
    # Giá trị khấu hao
    original_value = fields.Float('Giá trị ban đầu', required=True)
    depreciation_amount = fields.Float('Số tiền khấu hao tháng', required=True)
    remaining_value = fields.Float('Giá trị còn lại', compute='_compute_remaining_value', store=True)
    
    # Phương pháp khấu hao
    depreciation_method = fields.Selection([
        ('straight_line', 'Tuyến tính'),
        ('degressive', 'Giảm dần'),
    ], string='Phương pháp khấu hao', default='straight_line')
    
    # Trạng thái
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Xác nhận'),
        ('posted', 'Đã ghi sổ'),
    ], string='Trạng thái', default='draft')
    
    # Ghi chú
    notes = fields.Text('Ghi chú')
    
    # Link tới bút toán kế toán
    account_move_id = fields.Many2one('account.move.custom', string='Bút toán kế toán')

    @api.depends('date')
    def _compute_month(self):
        for record in self:
            if record.date:
                record.month = record.date.strftime('%m/%Y')

    @api.depends('original_value', 'depreciation_amount')
    def _compute_remaining_value(self):
        for record in self:
            record.remaining_value = record.original_value - record.depreciation_amount

    def action_confirm(self):
        """Xác nhận khấu hao"""
        self.state = 'confirmed'
        # Tự động tạo bút toán kế toán
        self._create_account_move()

    def _create_account_move(self):
        """Tự động tạo bút toán kế toán"""
        AccountMove = self.env['account.move.custom']
        for record in self:
            if not record.account_move_id:
                move = AccountMove.create({
                    'asset_id': record.asset_id.id,
                    'employee_id': record.employee_id.id,
                    'amount': record.depreciation_amount,
                    'date': record.date,
                    'description': f'Khấu hao {record.asset_id.ten_tai_san} - {record.month}',
                    'move_type': 'depreciation',
                })
                record.account_move_id = move.id
                move.action_post()

    def action_post(self):
        """Đăng ký bút toán"""
        if self.account_move_id:
            self.account_move_id.action_post()
        self.state = 'posted'
