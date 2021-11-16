# -*- coding: utf-8 -*-
{
    'name': "de_department_wise_ot_report",

    'summary': """
        Employee Overtime Report Deparmtent Wise
        
        
        
        """,

    'description': """
        Employee Overtime Report Deparmtent Wise
        1: some fields like employee name, employee type, number get from from hr.employee
        2: Employee ---- employee rest like ovt feeded hours, actual hours, etc get form overtime request
        3: Overtime ----> Operations--------> overtime request 
    """,

    'author': "Dynaxel",
    'website': "http://www.dynaxel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','de_employee_overtime','hr'],

    # always loaded
    'data': [
        'report/hr_employee_overtime_header.xml',
        'security/ir.model.access.csv',
        'wizard/hr_employee_overtime_wizard.xml',
        'report/hr_employee_overtime_view.xml',
        'report/hr_employee_overtime_template.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
