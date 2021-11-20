# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    fiscal_period = fields.Selection( 
        [
        ('1', 'Jan'),
        ('2', 'Feb'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'Jun'),
        ('7', 'July'),
        ('8', 'Aug'),
         ('9', 'Sep'),
        ('10', 'Oct'),
        ('11', 'Nov'),
        ('12', 'Dec'),    
         ],
         string='Fiscal Year', default='6')
    fiscalyear_last_day = fields.Integer(string='Days', default=30)
    
    
    

