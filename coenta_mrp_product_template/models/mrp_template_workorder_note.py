# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MrpTemplateWorkorderNote(models.Model):

    _name = "mrp.template.workorder.note"
    _description = "Mrp Template Workorder Note"  # TODO


    sequence = fields.Integer("Sequence", default=10)
    name = fields.Text("Production Note")

    mrp_template_id = fields.Many2one("mrp.product.template", string="Product Template", required=True)
    workorder_id = fields.Many2one("mrp.template.workorder", string="Work Order", required=True)
    workorder_ids = fields.One2many("mrp.template.workorder", related="mrp_template_id.workorder_template_ids", string="Work Orders")
    image = fields.Binary("Image")



