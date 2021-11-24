from odoo import models, fields, api


class ReconcileSummary(models.Model):
    _inherit = 'hr.salary.rule'
    
   

    reconcilation_compensation = fields.Boolean( string="Compensation")
    reconcilation_deduction = fields.Boolean( string="Deduction")
    
    
