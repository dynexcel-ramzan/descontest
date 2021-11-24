# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#
#################################################################################

from odoo import models, fields, api
from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta


class EmployeeEobi(models.TransientModel):
    _name = 'employee.eobi.wizard'
#     _description = 'de_payroll_tax_report.de_payroll_tax_report'

    employee_type = fields.Selection([('permanent','Permanent'),('contractor','Contractor'),('freelancer','Freelancer'),('intern','Intern'),('part time','Part Time'),('project based hiring','Project Based Hiring'),('outsourse','Outsourse')],string="Employee")
    department_id = fields.Many2one('hr.department', string="Department")
    location_id = fields.Many2one('hr.work.location',string="location")
    section_id = fields.Many2one('hr.employee',string="Section Type")
    


    def check_report(self):
        data = {}
        data['form'] = self.read()[0]
        return self.print_report(data)

    def print_report(self,data):
        data['form'].update(self.read()[0])
        return self.env.ref('de_employee_eobi_report.employee_eobi_wizard_action').report_action(self,data=data,config=False)
    
 

