# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MrpWorkorder(models.Model):

    _inherit = "mrp.workorder"



    workorder_template_id = fields.Many2one('mrp.template.workorder','Workorder Template')

    workorder_specifaction = fields.Char('Workorder Specifaction',related='workorder_template_id.name',store=True)