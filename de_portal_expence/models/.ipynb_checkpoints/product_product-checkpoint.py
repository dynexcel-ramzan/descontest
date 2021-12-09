# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    ora_category_id = fields.Many2one('ora.expense.category', string='Expense Category', required=True)
    meter_reading = fields.Float(string='Meter Reading')
    ora_unit = fields.Selection(selection=[
            ('amount', 'Amount'),
            ('km', 'Km'),
        ], string='Unit', required=True,
        )
    

