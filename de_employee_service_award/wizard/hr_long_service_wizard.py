# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class LongService(models.TransientModel):
    _name = "long.service.wizard"
    _description = "Long Service Report wizard"

    date = fields.Date(string='Date', required=True)
    department_ids = fields.Many2many('hr.department', string='department')
    employee_type_id = fields.Many2one('hr.employee', string='Emp Type')
    location_ids = fields.Many2many('hr.work.location', string='Location')
    section_ids = fields.Many2many('hr.employee', string='Section')
   

    
    def check_report(self):
        data = {}
        data['form'] = self.read(['date','department_ids','employee_type_id','location_ids','section_ids'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['date','department_ids','employee_type_id','location_ids','section_ids'])[0])
        return self.env.ref('de_employee_service_award.open_hr_long_service_action').report_action(self, data=data, config=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        