# -*- coding: utf-8 -*-
from odoo import models, fields, api

class NhanVienExtend(models.Model):
    _inherit = 'nhan_vien'

    tai_san_dang_giu_ids = fields.One2many(
        'phan_bo_tai_san', 'nhan_vien_su_dung_id', 
        string="Tài sản đang được cấp phát"
    )
    
    tai_san_dang_muon_ids = fields.One2many(
        'don_muon_tai_san', 'nhan_vien_muon_id',
        string="Tài sản đang mượn"
    )
