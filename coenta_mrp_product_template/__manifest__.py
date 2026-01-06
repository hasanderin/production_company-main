{
    'name': 'Coenta Mrp Product Template',
    'description': """
        Manage Productions with product Template""",
    'version': '15.0.1.0.1',
    'license': 'AGPL-3',
    'author': 'Coenta Team',
    'website': 'coenta.com',
    'depends': ['mrp','product','sale','sale_stock'
    ],
    'data': [
        'views/stock_picking.xml',
        'security/mrp_template_workorder_note.xml',
        'security/sale_production_note.xml',
        'views/product_attribute.xml',
        'security/mrp_product_template_move.xml',
        'views/mrp_workorder.xml',
        'security/mrp_template_workorder.xml',
        'views/mrp_template_workorder.xml',
        'views/sale_order.xml',
        'data/data.xml',
        'views/mrp_production.xml',
        'security/mrp_product_template.xml',
        'views/mrp_product_template.xml',
        'report/report.xml',
        'report/report_document.xml',
        'report/report_sale_production_note.xml',
        'security/mrp_product_template_rules.xml',

    ],
    'demo': [
    ],
}
