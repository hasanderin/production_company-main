# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class MrpTemplateWorkorder(models.Model):

    _name = "mrp.template.workorder"
    _description = "Mrp Template Workorder"  # TODO



    mrp_template_id = fields.Many2one('mrp.product.template','Template')
    name = fields.Char('Production Notes')
    production_id = fields.Many2one('mrp.production','Production')
    operation_id = fields.Many2one('mrp.routing.workcenter','Work Order')


    workorder_note_ids = fields.One2many('mrp.template.workorder.note','workorder_id','Work Order Notes')

    planned_start_date = fields.Datetime('Planned Start Date')
    planned_end_date = fields.Datetime('Planned End Date')

    workorder_note_count = fields.Integer(compute='_compute_workorder_note_count', string='Work Order Notes Count')

    @api.depends('workorder_note_ids')
    def _compute_workorder_note_count(self):
        for rec in self:
            if rec.workorder_note_ids:
                rec.workorder_note_count = len(rec.workorder_note_ids)
            else:
                rec.workorder_note_count =0

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name or rec.operation_id.name
            result.append((rec.id, name))
        return result


    workcenter_id = fields.Many2one('mrp.workcenter','Work Center')
    image = fields.Binary('Image')


    # def _compute_sale_information(self):
    #     for rec in self:
    #         if rec.mrp_template_id:
    #             rec.name = False
    #             rec.image = False
    #             rec.workcenter_id = False
    #             sale_id = rec.mrp_template_id.sale_id
    #             #filtered_sale_notes = sale_id.sale_production_note_ids.filtered(lambda x: x.product_template_id.id == rec.mrp_template_id.product_tmpl_id.id)
    #             #found = filtered_sale_notes.filtered(lambda x: x.workcenter_id.id == rec.operation_id.workcenter_id.id)
    #             # if found:
    #             #     found= found[0]
    #             #     rec.name = found.name
    #             #     rec.image = found.image
    #             #     rec.workcenter_id= found.workcenter_id.id
    #             # else:
    #             #     rec.name = False
    #             #     rec.workcenter_id = False
    #             #     rec.image = False
    #         else:
    #             rec.workcenter_id = False
    #             rec.image = False
    #             rec.name = False

    workorder_ids = fields.One2many('mrp.workorder','workorder_template_id','Work Orders')

    state = fields.Selection([
        ('pending', 'Pending'),
        ('waiting', 'Waiting'),
        ('ready', 'Ready'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='pending', track_visibility='onchange')

    production_state = fields.Selection(related="mrp_template_id.state",string='Production State',store=True)



    duration = fields.Float(
        'Real Duration', compute='_compute_duration',
        readonly=False,  copy=False)


    @api.depends('workorder_ids','workorder_ids.time_ids','workorder_ids.duration')
    def _compute_duration(self):
        for rec in self:
            rec.duration = 0
            if rec.workorder_ids:
                workorders = rec.workorder_ids.filtered(lambda x: x.state not in ['cancel'])
                if workorders:
                    rec.duration = sum(workorders.mapped('duration'))/len(workorders)


    def button_start(self):
        self.ensure_one()
        if not self.workorder_ids:
            raise UserError(_('No work orders to start.'))
        for workorder in self.workorder_ids:
            workorder.button_start()
            self.state= 'in_progress'
        if self.workorder_ids:
            self.mrp_template_id.state = 'in_progress'
        return True

    def button_pending(self):
        self.ensure_one()
        if not self.workorder_ids:
            raise UserError(_('No work orders to finish.'))
        for workorder in self.workorder_ids:
            workorder.button_pending()
        self.state = 'pending'
        return True

    def button_finish(self):
        self.ensure_one()
        if not self.workorder_ids:
            raise UserError(_('No work orders to end.'))
        for workorder in self.workorder_ids:
            workorder.button_finish()
        self.state = 'done'
        return True


    def print_report(self):
        self.ensure_one()
        action = self.env.ref('coenta_mrp_product_template.action_report_work_order').report_action(self)
        return action
