from odoo import models, fields, api
from odoo import models, fields, api
from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta
from odoo.exceptions import UserError



class TotalTaxCreditForm(models.TransientModel):
    _name = 'total.tax.credit.forms'
    _description = 'Total tax credit form'

    tax_company_id = fields.Many2one('res.company', string="Company")
    tax_period = fields.Date( string="Tax Period")
#     empl_code = fields.Many2one('hr.employee', string="Employee Code",
# #                                 related="tax_company_id.empl_code"
#                                )
    

    
    

  
    

