# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from datetime import datetime


class AssetAPIController(http.Controller):

    @http.route('/api/assets/overview', type='json', auth='user', methods=['GET'])
    def get_assets_overview(self):
        """API lấy tổng quan tài sản"""
        try:
            assets = request.env['tai_san'].search([])

            data = {
                'total_assets': len(assets),
                'total_value': sum(asset.gia_tri_ban_dau for asset in assets),
                'current_value': sum(asset.gia_tri_hien_tai for asset in assets),
                'depreciated_value': sum(asset.gia_tri_ban_dau - asset.gia_tri_hien_tai for asset in assets),
                'timestamp': datetime.now().isoformat()
            }

            return {'status': 'success', 'data': data}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/assets/depreciation', type='json', auth='user', methods=['POST'])
    def trigger_depreciation(self):
        """API trigger khấu hao hàng tháng"""
        try:
            # Chạy khấu hao cho tất cả tài sản
            request.env['tai_san'].schedule_monthly_depreciation()

            return {
                'status': 'success',
                'message': 'Monthly depreciation completed',
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/assets/ai-analysis', type='json', auth='user', methods=['GET'])
    def get_ai_analysis(self):
        """API lấy kết quả phân tích AI gần nhất"""
        try:
            latest_analysis = request.env['asset.ai.analysis'].search(
                [('state', '=', 'analyzed')],
                order='analysis_date desc',
                limit=1
            )

            if latest_analysis:
                data = {
                    'analysis_date': latest_analysis.analysis_date.isoformat(),
                    'total_assets': latest_analysis.total_assets,
                    'total_value': latest_analysis.total_value,
                    'average_depreciation': latest_analysis.average_depreciation,
                    'analysis_text': latest_analysis.analysis_text,
                    'recommendations': latest_analysis.recommendations,
                    'anomalies': latest_analysis.anomalies
                }
            else:
                data = {'message': 'No AI analysis available'}

            return {'status': 'success', 'data': data}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @http.route('/api/assets/external/sync', type='json', auth='user', methods=['POST'])
    def sync_external_data(self):
        """API đồng bộ dữ liệu từ bên ngoài (placeholder)"""
        try:
            # Placeholder for external API integration
            # Có thể tích hợp với Google Calendar, Telegram, etc.

            return {
                'status': 'success',
                'message': 'External sync completed (placeholder)',
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            return {'status': 'error', 'message': str(e)}
