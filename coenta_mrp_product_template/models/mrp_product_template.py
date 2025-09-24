# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class MrpProductTemplate(models.Model):
    _name = "mrp.product.template"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Mrp Product Template"  # TODO

    name = fields.Char('Name', default=lambda self: _('New'), required=True,copy=False)


    sale_id = fields.Many2one('sale.order','Sale')

    date_planned_start = fields.Datetime('Planned Start Date',default=lambda self: fields.Datetime.now())

    partner_id = fields.Many2one('res.partner', 'Customer', related='sale_id.partner_id', store=True)
    commitment_date = fields.Datetime('Commitment Date', related='sale_id.commitment_date', store=True)

    mrp_template_workorder_note_ids = fields.One2many('mrp.template.workorder.note', 'mrp_template_id', string='Workorder Notes')

    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        domain="[('code', '=', 'mrp_operation')]",
    )

    bom_id = fields.Many2one('mrp.bom', 'Bom')


    production_ids = fields.One2many('mrp.production', 'coenta_product_template_id', string='Productions')

    product_tmpl_id = fields.Many2one('product.template', string='Product Template',required=True)
    mrp_product_template_line_ids = fields.One2many('mrp.product.template.line', 'mrp_product_template_id', string='Product Template Lines')

    mrp_product_template_move_ids = fields.One2many('mrp.product.template.move', 'mrp_product_template_id', string='Product Template Moves')

    workorder_template_ids = fields.One2many('mrp.template.workorder', 'mrp_template_id', string='Workorder Template')

    in_progress_wo_ids = fields.Many2many("mrp.template.workorder",
                                         string="Work In Progress",
                                         compute='_compute_in_progress_workorder',store=True
                                         )

    @api.depends('workorder_template_ids', 'workorder_template_ids.state')
    def _compute_in_progress_workorder(self):
        for rec in self:
            in_pr_wo_ids = rec.workorder_template_ids.filtered(lambda l: l.state == 'in_progress')
            rec.in_progress_wo_ids = in_pr_wo_ids

    @api.onchange('product_tmpl_id')
    def _onchage_product_template_id(self):
        for rec in self:
            if rec.product_tmpl_id:
                rec.bom_id = rec.product_tmpl_id.bom_ids and rec.product_tmpl_id.bom_ids[0].id
            else:
                rec.bom_id = False

    quantity = fields.Float('Total Quantity',compute='_compute_quantity',store=True)
    done_qty = fields.Float('Done Quantity',compute='_compute_quantity',store=True)


    @api.depends('mrp_product_template_line_ids','mrp_product_template_line_ids.quantity','production_ids','production_ids.qty_produced')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = 0
            rec.done_qty =0
            if rec.mrp_product_template_line_ids:
                rec.quantity = sum(rec.mrp_product_template_line_ids.mapped('quantity'))
            if rec.production_ids:
                rec.done_qty = sum(rec.production_ids.mapped('qty_produced'))

    @api.model_create_multi
    def create(self, vals_list):
        res = super(MrpProductTemplate, self).create(vals_list)
        if res.name == _('New'):
            seq = self.env['ir.sequence'].next_by_code('mrp.product.template')
            res.name = seq
            res.button_get_lines()
        return res


    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')

    def button_get_lines(self):
        for rec in self:
            sale_order = self.env['sale.order'].search([('id', '=', rec.sale_id.id)])
            if sale_order:
                lines = sale_order.order_line.filtered(lambda l: l.product_id.product_tmpl_id.id == rec.product_tmpl_id.id)
                for line in lines:
                    self.env['mrp.product.template.line'].create({
                        'product_id': line.product_id.id,
                        'mrp_product_template_id':rec.id,
                        'quantity':line.product_uom_qty,
                    })


    def button_create_productions(self):
        for rec in self:
            if rec.bom_id:
                if rec.bom_id.operation_ids:
                    rec.workorder_template_ids = [(5, 0, 0)]
                    for operation in rec.bom_id.operation_ids:
                        self.env['mrp.template.workorder'].create({
                            'operation_id': operation.id,
                            'mrp_template_id': rec.id,
            })
                if rec.bom_id.bom_line_ids:
                    rec.mrp_product_template_move_ids = [(5, 0, 0)]
                    for line in rec.bom_id.bom_line_ids:
                        self.env['mrp.product.template.move'].create({
                            'product_id': line.product_id.id,
                            'mrp_product_template_id': rec.id,
                            'product_qty': line.product_qty,
                            'product_uom_id': line.product_uom_id.id,
                            'quantity_done':line.product_qty,
                            'operation_id': line.operation_id.id,
                            'bom_product_template_attribute_value_ids': [(6, 0, line.bom_product_template_attribute_value_ids.ids)],
                        })

        for line in rec.mrp_product_template_line_ids:
            if line.quantity:
                production = self.env['mrp.production'].create({
                    'product_id': line.product_id.id,
                    'product_qty': line.quantity,
                    'product_uom_id': line.product_id.uom_id.id,
                    'bom_id': rec.bom_id.id,
                    'coenta_product_template_id': rec.id,
                    'picking_type_id':rec.picking_type_id.id,
                    'date_planned_start': rec.date_planned_start,
                    'origin':rec.sale_id.name or "",
                })
                production._create_update_move_finished()
                production._onchange_move_raw()
                production._create_workorder()
                production._plan_workorders()
                production.action_confirm()
                for workorder in production.workorder_ids:
                    operation = rec.workorder_template_ids.filtered(lambda l: l.operation_id == workorder.operation_id)
                    if operation:
                        workorder.write({'workorder_template_id': operation[0].id})
                for move in production.move_raw_ids:
                    move.coenta_product_move_id = rec.mrp_product_template_move_ids.filtered(lambda l: l.product_id == move.product_id)[0].id

        for line in rec.sale_id.sale_production_note_ids:
            workorder = rec.workorder_template_ids.filtered(lambda l: l.operation_id.workcenter_id.id == line.workcenter_id.id)
            if line.product_template_id.id == rec.product_tmpl_id.id and workorder:
                self.env['mrp.template.workorder.note'].create({
                    'mrp_template_id': rec.id,
                    'workorder_id': workorder.id or False,
                    'name': line.name,
                    'image': line.image,
                })

        rec.state= 'confirmed'


    def button_mark_done(self):
        for rec in self:
            rec.state = 'done'
            for production in rec.production_ids:
                for move in production.move_raw_ids:
                    move.product_uom_qty = move.coenta_product_move_id.quantity_done * production.qty_producing
                    move.quantity_done = move.coenta_product_move_id.quantity_done * production.qty_producing
                if production.state == 'to_close':
                    production.with_context(skip_consumption=True).button_mark_done()
                else:
                    raise UserError(_('Production Orders are not completed yet'))


    def button_cancel_productions(self):
        for rec in self:
            for production in rec.production_ids:
                if production.state == 'confirmed':
                    production.action_cancel()
                # else:
                #     raise ValueError(_('Production %s is not in confirmed state' % production.name))
            rec.state = 'cancel'


    workorder_template_status = fields.Char('Workorder Template Status', compute='_compute_workorder_template_status')

    def _compute_workorder_template_status(self):
        for rec in self:
            if all(x.state == 'done' for x in rec.workorder_template_ids):
                rec.workorder_template_status = 'Tamamlandı'
            if rec.workorder_template_ids:
                rec.workorder_template_status = ', '.join(rec.workorder_template_ids.filtered(lambda x: x.state =='in_progress').mapped('operation_id.name'))
            else:
                rec.workorder_template_status = 'Başlamadı'


    def button_open_sale_id(self):
        return{
            'name': _('Sale Order'),
            'view_mode': 'form',
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'res_id': self.sale_id.id,
        }
