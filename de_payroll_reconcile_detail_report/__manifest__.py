# -*- coding: utf-8 -*-
{
    'name': "de_payroll_reconcile_detail_report",

    'summary': """
        Payroll Reconciliation detail      
        """,

    'description': """
        Payroll Reconciliation detail 
          user select  date from =  aug 2021 and  date to = sep2021 than payslip rule like overtime basic salary car allowance etc,
    """,

    'author': "My dynaxel",
    'website': "http://www.dynaxel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','de_employee_overtime'],

    # always loaded
    'data': [
        
        'report/hr_payroll_reconile_header.xml',
        'security/ir.model.access.csv',
        'wizard/hr_payroll_reconcile_wizard.xml',
        'report/hr_payroll_reconile_view.xml',
        'report/hr_payroll_reconile_template.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
