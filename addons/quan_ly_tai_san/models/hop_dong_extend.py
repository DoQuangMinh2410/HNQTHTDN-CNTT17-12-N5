# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HopDongExtend(models.Model):
    _inherit = 'hop_dong'

    def action_cham_dut(self):
        # Allow original logic to run
        res = super(HopDongExtend, self).action_cham_dut()
        
        # EVENT-DRIVEN AUTOMATION: Asset recovery when contract terminates
        for rec in self:
            nv = rec.nhan_vien_id
            if nv:
                # Tìm tài sản đang phân bổ cho nhân viên này
                phan_bo_dang_giu = self.env['phan_bo_tai_san'].search([
                    ('nhan_vien_su_dung_id', '=', nv.id),
                    ('trang_thai', 'in', ['dang_su_dung'])
                ])
                if phan_bo_dang_giu:
                    # Tạo cảnh báo hoặc tự động sinh phiếu thu hồi
                    # Ở đây ta gửi thông báo cho nhóm hành chính
                    self.env['bus.bus']._sendone(
                        self.env.user.partner_id,
                        'simple_notification',
                        {
                            'title': 'Cảnh báo thu hồi tài sản!',
                            'message': f'Nhân viên {nv.ho_ten} vừa chấm dứt hợp đồng, vui lòng kiểm tra và thu hồi {len(phan_bo_dang_giu)} tài sản đang cấp phát!',
                            'type': 'warning'
                        }
                    )
        return res
