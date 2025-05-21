# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleProductionNote(models.Model):

    _name = "sale.production.note"
    _description = "Sale Production Note"  # TODO


    sequence = fields.Integer("Sequence", default=10)
    name = fields.Text("Production Note")

    sale_id = fields.Many2one("sale.order", string="Sale Order", required=True)

    product_template_id = fields.Many2one("product.template" , string="Product Template", required=True)

    #workcenter_id = fields.Many2one("mrp.workcenter", string="Work Center", required=True)

    image = fields.Binary("Image")


    domain_product_template_ids = fields.Many2many("product.template", related="sale_id.domain_product_template_ids", string="Domain Product Template")


