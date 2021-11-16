# -*- coding: utf-8 -*-
{
    'name': "Overtime Report",

    'summary': """
        Overtime Report Locationwise and Department Wise
        """,

    'description': """
        Overtime Report Locationwise and Department Wise
        1- Report printed between specific period.
        2- 'hr.overtime.entry'  
        3- Location EMployee Record printed.
        
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HRMS/Overtime',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','de_employee_overtime','hr_payroll'],

    # always loaded
    'data': [
        'report/hr_overtime_report-header.xml',
        'security/ir.model.access.csv',
        'wizard/hr_overtime_wizard.xml',
        'report/hr_overtime_report.xml',
        'report/hr_overtime_report_template.xml',
        'views/hr_payroll_report_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
