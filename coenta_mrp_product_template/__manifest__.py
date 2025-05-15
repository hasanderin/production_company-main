{
    'name': 'Coenta Mrp Product Template',
    'description': """
        Manage Productions with product Template""",
    'version': '15.0.1.0.1',
    'license': 'AGPL-3',
    'author': 'Coenta Team',
    'website': 'coenta.com',
    'depends': ['mrp','product','sale'
    ],
    'data': [
        'views/mrp_workorder.xml',
        'security/mrp_template_workorder.xml',
        'views/mrp_template_workorder.xml',
        'views/sale_order.xml',
        'data/data.xml',
        'views/mrp_production.xml',
        'security/mrp_product_template.xml',
        'views/mrp_product_template.xml',
    ],
    'demo': [
    ],
}
