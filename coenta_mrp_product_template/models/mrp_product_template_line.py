# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MrpProductTemplateLine(models.Model):

    _name = "mrp.product.template.line"
    _description = "Mrp Product Template Line"  # TODO



    mrp_product_template_id = fields.Many2one('mrp.product.template', string='Product Template')
    product_id = fields.Many2one('product.product', string='Product')
    quantity = fields.Float(string='Quantity')
