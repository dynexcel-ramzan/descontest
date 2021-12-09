# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    chanceller_id = fields.Many2one('hr.employee', string='Vice-Chancellor')
    finance_partner_id = fields.Many2one('hr.employee', string='FBP')
    shared_finance_partner_id = fields.Many2one('hr.employee', string='Shared Service Finance')
    is_fbp_approval = fields.Boolean(string='FBP Approval')
    

