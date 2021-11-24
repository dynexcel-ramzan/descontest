# -*- coding: utf-8 -*-
{
    'name': "de_computation_tax_report",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_work_entry_contract'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/tax_computation_sheet.xml',
        'reports/computation_report_tax.xml',
        'reports/computation_tax_register.xml',
        'views/computation_tax.xml',
#         'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
