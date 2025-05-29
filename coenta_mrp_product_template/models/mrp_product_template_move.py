# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MrpProductTemplateMove(models.Model):

    _name = "mrp.product.template.move"
    _description = "Mrp Product Template Move"  # TODO


    mrp_product_template_id = fields.Many2one('mrp.product.template', 'Product Template')
    product_id = fields.Many2one('product.product', 'Product')
    product_qty = fields.Float('Product Quantity')
    product_uom_id = fields.Many2one('uom.uom', 'Product UoM')
    quantity_done = fields.Float('Quantity Done')
    operation_id = fields.Many2one('mrp.routing.workcenter','Operation')

    bom_product_template_attribute_value_ids = fields.Many2many(
        'product.template.attribute.value', string="Apply on Variants", ondelete='restrict',
        readonly=1,
        help="BOM Product Variants needed to apply this line.")
