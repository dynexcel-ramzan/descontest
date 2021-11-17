from odoo import models, fields, api
from odoo import models, fields, api
from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta


class TaxCreditForm(models.TransientModel):
    _name = 'tax.credit.forms'
    _description = 'de tax credit form'

    company = fields.Many2one('res.partner', string="Company")
    tax_period = fields.Date( string="Tax Period")
    emp_code = fields.Char( string="Employee Code")
    
    
    def tax_income(self):
        action = self.env["ir.actions.actions"]._for_xml_id("de_tax_credit_form.open_computation_tax_register_action")
        return action
        
       
        
