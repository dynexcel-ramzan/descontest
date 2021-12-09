# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class GradeDesignation(models.Model):
    _inherit = 'grade.designation.line'
    
    
    ora_unit = fields.Selection(selection=[
            ('amount', 'Amount'),
            ('km', 'Km'),
        ], string='Unit', required=True,
        )
    
    
    @api.onchange('expense_type')
    def onchange_expense_type(self):
        for line in self:
            if line.expense_type:
                line.ora_unit = line.expense_type.ora_unit
        
    
        

