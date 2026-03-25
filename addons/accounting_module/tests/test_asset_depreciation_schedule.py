from odoo.tests.common import TransactionCase
from odoo import fields


class TestAssetDepreciationSchedule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.category = self.env['danh_muc_tai_san'].create({
            'ma_danh_muc_ts': 'MTC',
            'ten_danh_muc_ts': 'Máy tính',
        })

    def test_schedule_monthly_depreciation_integration(self):
        asset = self.env['tai_san'].create({
            'ma_tai_san': 'TS-001',
            'ten_tai_san': 'Laptop Test',
            'ngay_mua_ts': fields.Date.today(),
            'don_vi_tien_te': 'vnd',
            'gia_tri_ban_dau': 1000000,
            'gia_tri_hien_tai': 1000000,
            'danh_muc_ts_id': self.category.id,
            'pp_khau_hao': 'straight-line',
            'thoi_gian_toi_da': 5,
            'don_vi_tinh': 'Chiếc',
        })

        schedule = self.env['asset.depreciation.schedule'].create({
            'asset_id': asset.id,
            'original_value': asset.gia_tri_ban_dau,
            'useful_life_months': 5,
            'start_date': fields.Date.today(),
            'depreciation_method': 'straight_line',
            'is_active': True,
        })

        self.assertEqual(schedule.monthly_depreciation, 200000.0)
        self.assertEqual(schedule.total_depreciation_periods, 5)

        self.env['tai_san'].schedule_monthly_depreciation()

        asset.refresh()
        self.assertEqual(asset.gia_tri_hien_tai, 0.0)

        depreciation_records = self.env['asset.depreciation'].search([('asset_id', '=', asset.id)])
        self.assertEqual(len(depreciation_records), 5)

        history_records = self.env['lich_su_khau_hao'].search([('ma_ts', '=', asset.id)])
        self.assertEqual(len(history_records), 5)
