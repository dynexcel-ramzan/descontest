# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LeaveLedger(models.Model):
    _inherit = 'hr.employee'
    
    section_ids = fields.Many2many('leave.ledger.wizard', string='Leave Ledger Report wizard')   

    
    
# class LeaveLedger(models.Model):
#     _inherit = 'hr.department'
    
#     department_ids = fields.Many2many('leave.ledger.wizard', string='Leave Ledger Report wizard')   
    
    
    
    
