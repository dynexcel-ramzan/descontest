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

    company_id = fields.Many2one('res.partner', string="Company")
    tax_period = fields.Date( string="Tax Period")
    emp_code = fields.Char( string="Employee Code")
    
    
    
    def tax_investment(self):
            
        return {
            'name': ('Investment Tax'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'tax.credit',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_company_id': self.company_id.ids , 'default_tax_period': self.tax_period, 'default_emp_code': self.emp_code },
        }
    
  
    
   







#     def tax_income(self):
#         action = self.env["ir.actions.actions"]._for_xml_id("de_tax_credit_form.open_computation_tax_register_action")
#         return action
        
       
        
