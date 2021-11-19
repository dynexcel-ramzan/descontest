from odoo import models, fields, api
from odoo import models, fields, api
from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta
from odoo.exceptions import UserError



class TaxCreditForm(models.TransientModel):
    _name = 'tax.credit.forms'
    _description = 'de tax credit form'

    company_id = fields.Many2one('res.company', string="Company")
    tax_period = fields.Date( string="Tax Period")
    empl_code = fields.Char( string="Employee")
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                domain="[('company_id.id','=',company_id)]")
    

    
#      def taxable_income(self):
#             wage = 0
#             benefit = 0
            
#              tot_tax_income = self.env['hr.contract'].search([('wage', '=', self.investment_amount)])
#              wage = tot_tax_income.wage
#             for f in tot_tax_income.benefit_line_ids:
#                 benfit = f.amount + benfit
                
#             return wage + benefit
    
    
    
    def tax_investment(self):
            
        return {
            'name': ('Investment Tax'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'tax.credit',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_company_id': self.company_id.ids , 'default_tax_period': self.tax_period, 'default_employee_id': self.employee_id.id },
        }
        
