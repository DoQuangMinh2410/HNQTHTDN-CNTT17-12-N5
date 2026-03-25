# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AssetAssignment(models.Model):
    _name = 'asset.assignment'
    _description = 'Gán tài sản cho nhân viên'
    _rec_name = 'asset_id'

    asset_id = fields.Many2one('tai_san', string='Tài sản', required=True, ondelete='cascade')
    employee_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True, ondelete='cascade')
    
    assignment_date = fields.Date('Ngày gán', required=True, default=fields.Date.today)
    end_date = fields.Date('Ngày thu hồi')
    
    state = fields.Selection([
        ('assigned', 'Đã gán'),
        ('returned', 'Đã thu hồi'),
        ('damaged', 'Hư hỏng'),
    ], string='Trạng thái', default='assigned')
    
    notes = fields.Text('Ghi chú')
    
    def action_return_asset(self):
        """Thu hồi tài sản"""
        self.state = 'returned'
        self.end_date = fields.Date.today()
    
    def action_mark_damaged(self):
        """Đánh dấu hư hỏng"""
        self.state = 'damaged'
