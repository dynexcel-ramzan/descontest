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

    tax_company_id = fields.Many2one('res.company', string="Company")
    tax_period = fields.Date( string="Tax Period")
    empl_code = fields.Char( string="Employee")
#     empl_code = fields.Many2one('hr.employee', string="Employee Code",
# #                                 related="tax_company_id.empl_code"
#                                )
    
    
    
    def tax_investment(self):
            
        return {
            'name': ('Investment Tax'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'tax.credit',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_tax_company_id': self.tax_company_id.ids , 'default_tax_period': self.tax_period, 'default_emp_code': self.empl_code },
        }
        
