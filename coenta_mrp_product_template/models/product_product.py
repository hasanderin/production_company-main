# Copyright 2025 Coenta TEam
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProductProduct(models.Model):

    _inherit = "product.product"



    product_size_attribute_id = fields.Many2one('product.attribute.value', compute='_compute_size_id', string='Size Attribute')
    product_color_attribute_id = fields.Many2one('product.attribute.value', compute='_compute_size_id', string='Color Attribute')

    @api.depends('product_template_attribute_value_ids')
    def _compute_size_id(self):
        size_id = self.env['product.attribute'].search([('is_size', '=', True)], limit=1)
        color_id = self.env['product.attribute'].search([('is_color', '=', True)], limit=1)
        for product in self:
            if product.product_template_attribute_value_ids:
                size_attribute_value = product.product_template_attribute_value_ids.filtered(
                    lambda l: l.attribute_line_id.attribute_id.id == int(size_id))
                if size_attribute_value and size_attribute_value.product_attribute_value_id:
                    product.product_size_attribute_id = size_attribute_value.product_attribute_value_id.id
                else:
                    product.product_size_attribute_id = False
            else:
                product.product_size_attribute_id = False
            if product.product_template_attribute_value_ids:
                color_attribute_value = product.product_template_attribute_value_ids.filtered(
                    lambda l: l.attribute_line_id.attribute_id.id == int(color_id))
                if color_attribute_value and color_attribute_value.product_attribute_value_id:
                    product.product_color_attribute_id = color_attribute_value.product_attribute_value_id.id
                else:
                    product.product_color_attribute_id = False
            else:
                product.product_color_attribute_id = False