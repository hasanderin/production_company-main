# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class MrpProductTemplate(models.Model):

    _name = "mrp.product.template"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Mrp Product Template"  # TODO

    name = fields.Char('Name', default=lambda self: _('New'), required=True,copy=False)


    sale_id = fields.Many2one('sale.order','Sale')



    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        domain="[('code', '=', 'mrp_operation')]",
    )

    bom_id = fields.Many2one('mrp.bom', 'Bom')


    production_ids = fields.One2many('mrp.production', 'coenta_product_template_id', string='Productions')

    product_tmpl_id = fields.Many2one('product.template', string='Product Template',required=True)
    mrp_product_template_line_ids = fields.One2many('mrp.product.template.line', 'mrp_product_template_id', string='Product Template Lines')

    workorder_template_ids = fields.One2many('mrp.template.workorder', 'mrp_template_id', string='Workorder Template')

    @api.onchange('product_tmpl_id')
    def _onchage_product_template_id(self):
        for rec in self:
            if rec.product_tmpl_id:
                rec.bom_id = rec.product_tmpl_id.bom_ids and rec.product_tmpl_id.bom_ids[0].id
            else:
                rec.bom_id = False

    quantity = fields.Float('Total Quantity',compute='_compute_quantity',store=True)
    done_qty = fields.Float('Done Quantity',compute='_compute_quantity',store=True)

    order_sequence = fields.Selection([('initial', 'Initial'), ('first_recut', 'First Re-Cut'),
                                       ('second_recut', 'Second Re-Cut')], string='Order Sequence', default='initial')

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
            for line in rec.mrp_product_template_line_ids:
                if line.quantity:
                    production = self.env['mrp.production'].create({
                        'product_id': line.product_id.id,
                        'product_qty': line.quantity,
                        'product_uom_id': line.product_id.uom_id.id,
                        'bom_id': rec.bom_id.id,
                        'coenta_product_template_id': rec.id,
                        'picking_type_id':rec.picking_type_id.id,
                    })
                    production._create_workorder()
                    production._plan_workorders()
                    production.action_confirm()
                    for workorder in production.workorder_ids:
                        operation = rec.workorder_template_ids.filtered(lambda l: l.operation_id  == workorder.operation_id)
                        if operation:
                            workorder.write({'workorder_template_id': operation.id})

            rec.state= 'confirmed'


    def button_mark_done(self):
        for rec in self:
            rec.state = 'done'


    def button_cancel_productions(self):
        for rec in self:
            for production in rec.production_ids:
                if production.state == 'confirmed':
                    production.action_cancel()
                # else:
                #     raise ValueError(_('Production %s is not in confirmed state' % production.name))
            rec.state= 'cancel'


    @api.onchange('bom_id')
    def _onchange_bom_id(self):
        for rec in self:
            if rec.bom_id:
                if rec.bom_id.operation_ids:
                    rec.workorder_template_ids = [(5, 0, 0)]
                    for operation in rec.bom_id.operation_ids:
                        self.env['mrp.template.workorder'].create({
                            'operation_id': operation.id,
                            'mrp_template_id': rec.id,
                        })