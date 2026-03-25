/** @odoo-module **/

import { registry } from "@web/core/registry";
const { Component } = owl;
const { useState, onWillStart } = owl.hooks;
import { useService } from "@web/core/utils/hooks";

class Dashboard extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.state = useState({
            stats: {
                total_assets: 0,
                pending_orders: 0,
                borrowed_assets: 0,
                total_value: 0,
            },
            loading: false,
        });

        onWillStart(async () => {
            await this.fetchStats();
        });
    }

    async fetchStats() {
        this.state.loading = true;
        try {
            // Fetch Asset Counts
            const totalAssets = await this.rpc("/web/dataset/call_kw/tai_san/search_count", {
                model: "tai_san",
                method: "search_count",
                args: [[]],
                kwargs: {},
            });

            // Fetch Pending Purchase Requests
            const pendingPurchases = await this.rpc("/web/dataset/call_kw/yeu_cau_mua_sam/search_count", {
                model: "yeu_cau_mua_sam",
                method: "search_count",
                args: [[['trang_thai', '=', 'cho_duyet']]],
                kwargs: {},
            });

            // Fetch Pending Salaries
            const pendingSalaries = await this.rpc("/web/dataset/call_kw/tinh_luong/search_count", {
                model: "tinh_luong",
                method: "search_count",
                args: [[['trang_thai', '=', 'nhap']]], // Assuming 'nhap' is pending for salary
                kwargs: {},
            });

            // Fetch Borrowed Assets
            const borrowedCount = await this.rpc("/web/dataset/call_kw/muon_tra_tai_san/search_count", {
                model: "muon_tra_tai_san",
                method: "search_count",
                args: [[['trang_thai', '=', 'dang-muon']]],
                kwargs: {},
            });

            // Fetch Total Value
            const assetsResult = await this.rpc("/web/dataset/call_kw/tai_san/read_group", {
                model: "tai_san",
                method: "read_group",
                args: [[]],
                kwargs: {
                    fields: ["gia_tri_hien_tai"],
                    groupby: [],
                },
            });

            this.state.stats.total_assets = totalAssets;
            this.state.stats.pending_orders = pendingPurchases + pendingSalaries;
            this.state.stats.borrowed_assets = borrowedCount;
            this.state.stats.total_value = (assetsResult && assetsResult[0] && assetsResult[0].gia_tri_hien_tai) || 0;

        } catch (e) {
            console.error("Dashboard Fetch Error", e);
        } finally {
            this.state.loading = false;
        }
    }

    formatCurrency(value) {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
    }

    onAction(actionXmlId) {
        this.action.doAction(actionXmlId);
    }

    onCreate(model) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: model,
            views: [[false, 'form']],
            target: 'new',
        });
    }
}

Dashboard.template = "q_trang_chu.Dashboard";

registry.category("actions").add("q_trang_chu.dashboard", Dashboard);

export default Dashboard;
