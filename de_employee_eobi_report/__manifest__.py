# -*- coding: utf-8 -*-
{
    'name': "de_employee_eobi_report",

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
    'depends': ['base','hr_payroll', 'de_employee_enhancement','de_employee_overtime','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/employee_eobi_wizard.xml',
        'reports/employee_eobi_report_template.xml',
        'reports/employee_eobi_report.xml',
        
#         'views/views.xml',
#         'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}