# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class EmployeeEmial(models.TransientModel):
    _name = "employee.email.wizard"
    _description = "Employee Email Report wizard"

    company_id = fields.Many2many('hr.employee', string='company')
   
    def check_report(self):
        data = {}
        data['form'] = self.read(['company_id'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['company_id'])[0])
        return self.env.ref('de_employee_email_report.open_hr_employee_email_report').report_action(self, data=data, config=False)