# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class MrpTemplateWorkorder(models.Model):

    _name = "mrp.template.workorder"
    _description = "Mrp Template Workorder"  # TODO



    mrp_template_id = fields.Many2one('mrp.product.template','Template')
    name = fields.Char('Description')
    production_id = fields.Many2one('mrp.production','Production')
    operation_id = fields.Many2one('mrp.routing.workcenter','Work Order')


    workorder_ids = fields.One2many('mrp.workorder','workorder_template_id','Work Orders')


    def button_start(self):
        self.ensure_one()
        if not self.workorder_ids:
            raise UserError(_('No work orders to start.'))
        for workorder in self.workorder_ids:
            workorder.button_start()
        return True

    def button_pause(self):
        self.ensure_one()
        if not self.workorder_ids:
            raise UserError(_('No work orders to finish.'))
        for workorder in self.workorder_ids:
            workorder.button_pause()
        return True

    def button_finish(self):
        self.ensure_one()
        if not self.workorder_ids:
            raise UserError(_('No work orders to end.'))
        for workorder in self.workorder_ids:
            workorder.button_finish()
        return True