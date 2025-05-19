# Copyright 2025 Coenta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class StockMove(models.Model):

    _inherit = "stock.move"



    coenta_product_move_id = fields.Many2one('mrp.product.template.move', 'Product Move')