# Copyright 2025 Coenta Team
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"


    mrp_product_template_ids = fields.One2many('mrp.product.template','sale_id','Production Templates')

    sale_production_note_ids = fields.One2many('sale.production.note', 'sale_id', string="Production Notes")

    domain_product_template_ids = fields.Many2many("product.template",compute='_compute_domain_product_template_ids', string="Domain Product Template")

    @api.depends('order_line.product_id.product_tmpl_id')
    def _compute_domain_product_template_ids(self):
        for record in self:
            product_template_ids = record.order_line.mapped('product_id').mapped('product_tmpl_id')
            record.domain_product_template_ids = [(6, 0, product_template_ids.ids)]


    def create_mrp_product_template_ids(self):
        for record in self:
            templates = record.order_line.mapped('product_id').mapped('product_tmpl_id')
            for template in templates:
                mrp_production_template_id = self.mrp_product_template_ids.create({
                    'product_tmpl_id': template.id,
                    'sale_id': record.id
                })



    def action_open_product_template(self):
        self.ensure_one()
        action = self.env.ref('coenta_mrp_product_template.mrp_product_template_act_window').read()[0]
        if len(self.mrp_product_template_ids) == 1:
            action['views'] = [(self.env.ref('coenta_mrp_product_template.mrp_product_template_form_view').id, 'form')]
            action['res_id'] = self.mrp_product_template_ids[0].id
        else:
            action['views'] = [(self.env.ref('coenta_mrp_product_template.mrp_product_template_tree_view').id, 'tree'),
                               (self.env.ref('coenta_mrp_product_template.mrp_product_template_form_view').id, 'form')]
            action['domain'] = [('id', 'in', self.mrp_product_template_ids.ids)]
        return action


    def create_sale_production_notes(self):
        for record in self:
            templates = record.order_line.mapped('product_id').mapped('product_tmpl_id')
            for template in templates:
                self.env['sale.production.note'].create({
                    'sale_id': record.id,
                    'product_template_id': template.id,
                })




    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            record.create_sale_production_notes()
        return res