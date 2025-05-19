# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProductAttribute(models.Model):

    _inherit = "product.attribute"


    is_size = fields.Boolean("Is Size", default=False)
    is_color = fields.Boolean("Is Color", default=False)
