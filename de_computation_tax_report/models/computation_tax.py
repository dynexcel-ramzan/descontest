from odoo import models, fields, api


class de_computation_tax_report(models.Model):
    _name = 'computation.tax'
    _description = 'de computation tax report '

    taxable_income = fields.Char(string="taxable_income")
    rate = fields.Char(string="Rate %")
    
    
   

