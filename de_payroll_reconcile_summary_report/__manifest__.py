# -*- coding: utf-8 -*-
{
    'name': "de_payroll_reconcile_summary_report",

    'summary': """
  Payslip search within wizard date range and just sum  rule amount for all company employee.

""",

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
        'wizard/payroll_reconcile_wizard.xml',
        'report/payroll_reconcile_report_template.xml',
        'report/payroll_reconcile_report.xml',
        'views/views.xml',
#         'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}