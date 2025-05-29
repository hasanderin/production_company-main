# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MrpProduction(models.Model):

    _inherit = "mrp.production"



    coenta_product_template_id = fields.Many2one('mrp.product.template', string='Product Template')


