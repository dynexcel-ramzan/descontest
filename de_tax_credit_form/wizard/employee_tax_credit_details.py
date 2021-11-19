from odoo import models, fields, api
from odoo import models, fields, api
from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta
from odoo.exceptions import UserError



class TaxCreditDetails(models.TransientModel):
    _name = 'tax.credit.details'
    _description = 'de tax credit details'

    company_id = fields.Many2one('res.company', string="Company")
    tax_period = fields.Date( string="Tax Period")
    empl_code = fields.Char( string="Employee")
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                domain="[('company_id.id','=',company_id)]") 
    company_id = fields.Many2one('res.company', string="Company")
    emp_number = fields.Many2one('hr.employee', string="Employ Code")
    date_from = fields.Many2one('hr.payslip', string="Periods")
    tax_credit_line = fields.One2many('tax.credit.details.lines', 'credit_details_id', string='Employee Tax credit details')
    
    
    @api.onchange('employee_id')
    def onchange_credit(self):
        
        self.empl_code = self.employee_id.emp_number
        return 
    
    
#         employees = []
#         employees = self.env['tax.credit.forms'].search([], limit=1)
            
#         vals = { 
#                 'company_id':  employees,
#                 'employee_id': employees,
#         }
#               self.env['hr.employee'].create(vals)
            
class TaxCreditDetailsLines(models.TransientModel):
    _name = 'tax.credit.details.lines'
    _description = 'Tax credit details lines'

    credit_details_id = fields.Many2one('tax.credit.details', string='credit details id')
    company_id = fields.Many2one('res.company', string="Company")
    emp_number = fields.Many2one('hr.employee', string="Employ Code")
    date_from = fields.Many2one('hr.payslip', string="Periods")

            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            

    
    
#     def TaxxCredit(self, docids, data=None):
#         docs = self.env['tax.credit.forms'].browse(self.env.context.get('active_id'))
#         employees = self.env['hr.employee'].search([], limit=1)

#         if docs.company_id and docs.employee_id:
#             employees = self.env['hr.employee'].search(
#                 [('company_id', '=', docs.company_id.id), ('employee_id', '=', docs.employee_id.id)])

#         elif docs.employee_id:
#             employees = self.env['hr.employee'].search([('employee_id', '=', docs.employee_id.id)], )

#         elif docs.company_id:
#             employees = self.env['hr.employee'].search([('company_id', '=', docs.company_id.id)], )

#         return {
#             'docs': docs,
#             'employees': employees,
#         }    
    
    
    
#     def tax_investment(self):
            
#         return {
#             'name': ('Investment Tax'),
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'tax.credit',
#             'view_id': False,
#             'type': 'ir.actions.act_window',
#             'target': 'new',
#             'context': {'default_company_id': self.company_id.ids , 'default_tax_period': self.tax_period, 'default_employee_id': self.employee_id.id },
#         }
        
