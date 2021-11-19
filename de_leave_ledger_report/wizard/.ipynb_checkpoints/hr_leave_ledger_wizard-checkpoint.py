# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class LeaveLedger(models.TransientModel):
    _name = "leave.ledger.wizard"
    _description = "Leave Ledger Report wizard"

    
    
    department_ids = fields.Many2many('hr.department', string='department')
    employee_type_id = fields.Many2one('hr.employee', string='Employee')
    section_ids = fields.Many2many('hr.employee', string='Section')
    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    sorted_by = fields.Char(string='Sorted by')
    company_id = fields.Many2many('res.company', string='Company')
   

    
    def check_report(self):
        data = {}
        data['form'] = self.read(['department_ids','employee_type_id','section_ids','date_from','date_to','sorted_by'])[0]
        return self._print_report(data)

    def _print_report(self, data):
        data['form'].update(self.read(['department_ids','employee_type_id','section_ids','date_from','date_to','sorted_by',])[0])
        return self.env.ref('de_leave_ledger_report.open_hr_leave_ledger_action').report_action(self, data=data, config=False)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        