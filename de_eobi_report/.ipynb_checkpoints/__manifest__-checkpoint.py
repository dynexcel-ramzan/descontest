# -*- coding: utf-8 -*-
{
    'name': "de_eobi_report",

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
    'depends': ['base','hr_payroll', 'de_employee_overtime'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/eobi_report_wizard.xml',
        'reports/eobi_reports.xml',
        'reports/eobi_reports_template.xml',
        
#         'views/views.xml',
#         'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
