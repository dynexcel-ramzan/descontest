# -- coding: utf-8 --
{
    'name': "Tax Certificate Report",

    'summary':'Tax Certificate report of employees .Shows the total amount', 

    'description': """
        It will open from the  Payroll module:
    1) Click on the Reporting menu
    2) by clicking on tax Certificate , a wizard will open 
    having fields of employee names whose payslip exists in accounts move 
    model. For matching the time period "date to" field also exists in wizard.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Payroll',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','de_employee_enhancement','hr_attendance','hr_payroll_account','de_employee_loan','de_employee_overtime'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_tax_register_views.xml',
        'reports/purchase_tax_report.xml',
        'reports/purchase_tax_register_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
