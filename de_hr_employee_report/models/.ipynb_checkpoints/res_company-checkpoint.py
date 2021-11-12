from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'
    _description = 'Inherit Res Company'
    
    retirement_age = fields.Integer(string="Retirement Age",default=60)