# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrContract(models.Model):
    _inherit = 'hr.contract'
    
#     @api.onchange('wage')
#     def onchange_wage(self):
#         for contract in self:
#             promotion_vals={
#                 'employee_id': contract.employee_id.id,
#                 'contract_id': contract.id,
#                 'previous_salary':contract.wage,
#                 'previous_designation': contract.employee_id.job_id.id,
#                 'old_department': contract.employee_id.department_id.id,
#                 'date': 
#             }    
    
    
    

