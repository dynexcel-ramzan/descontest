# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    member_id = fields.Many2one('hr.employee.family', string='Dependent', domain="[('employee_id','=',employee_id)]")
    

