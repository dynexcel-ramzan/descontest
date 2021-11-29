# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BatchPayslip(models.Model):
    _inherit = 'hr.payslip.run'
    
    bank_id = fields.Many2one('banks.model', string='Bank Wizard')
