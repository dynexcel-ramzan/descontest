# -*- coding: utf-8 -*-
{
    'name': "Employee service award",

    'summary': """
        Create the Employee's long service report
        Create menu in the employee app under the report menu with the name of Long Service Award
        
        
        """,

    'description': """
        Create a wizard which contain the following information:
        Date : Mandatory
        Company : Mandatory
        Department: Optional if selected only print the department related employees else all employees
        Location: Optional if selected only print the department related employees else all employees
        DOP = DOJ (date of joining)
        Period should be as you can see in the report i.e. 12Y-3M-15D (where Y = Year, M = Month and D= Days)
        
        
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
        'report/hr_long_service_award_header.xml',
        'security/ir.model.access.csv',
        'wizard/hr_long_service_wizard.xml',
        'report/hr_long_service_award_view.xml',
        'report/hr_long_service_award_template.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installation': True,
    'auto_install': False,
}
