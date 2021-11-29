# -*- coding: utf-8 -*-
{
    'name': "de_leave_ledger_report",

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
    'depends': ['base','hr',],

    # always loaded
    'data': [
        'report/hr_leave_ledger_header.xml',
        'security/ir.model.access.csv',
        'wizard/hr_leave_ledger_wizard.xml',
        'report/hr_leave_ledger_view.xml',
        'report/hr_leave_ledger_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
