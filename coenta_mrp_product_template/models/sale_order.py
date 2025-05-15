# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"


    mrp_product_template_ids = fields.One2many('mrp.product.template','sale_id','Production Templates')


    def create_mrp_product_template_ids(self):
        for record in self:
            templates = record.order_line.mapped('product_id').mapped('product_tmpl_id')
            for template in templates:
                self.mrp_product_template_ids.create({
                    'product_tmpl_id': template.id,
                    'sale_id': record.id,
                })




