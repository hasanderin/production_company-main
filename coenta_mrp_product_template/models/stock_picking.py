# Copyright 2025 Coenta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class StockPicking(models.Model):

    _inherit = "stock.picking"


    mrp_product_template_ids = fields.Many2many('mrp.product.template', string='Model Üretim Emri',
                                                compute='_compute_mrp_product_template_ids',store=True)

    @api.depends('move_lines', 'move_lines.sale_line_id', 'move_lines.sale_line_id.order_id',
                 'move_lines.sale_line_id.order_id.mrp_product_template_ids')
    def _compute_mrp_product_template_ids(self):
        for record in self:
            mrp_product_template_ids = record.mapped('move_lines.sale_line_id.order_id.mrp_product_template_ids')
            record.mrp_product_template_ids = [(6, 0, mrp_product_template_ids.ids)]

