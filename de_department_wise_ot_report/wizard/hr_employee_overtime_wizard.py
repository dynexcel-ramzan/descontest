# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class DepartmentWise(models.TransientModel):
    _name = "department.wise.wizard"
    _description = "Department Wise Report wizard"

    date_from = fields.Date(string='Date form', required=True)
    date_to = fields.Date(string='Date to', required=True)
    location_ids = fields.Many2many('hr.work.location', string='Location')
    department_ids = fields.Many2many('hr.department', string='department')
    section_ids = fields.Many2many('hr.employee', string='Section')
    employee_type_id = fields.Many2one('hr.employee', string='Emp Type')
   

    
    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from','date_to','location_ids','department_ids','section_ids','employee_type_id'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date_from','date_to','location_ids','department_ids','section_ids','employee_type_id',])[0])
        return self.env.ref('de_department_wise_ot_report.open_hr_employee_overtime_action').report_action(self, data=data, config=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        