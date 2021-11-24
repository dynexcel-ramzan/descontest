# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    fiscal_period = fields.Selection( 
        [
        ('01', 'Jan'),
        ('02', 'Feb'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'Jun'),
        ('07', 'July'),
        ('08', 'Aug'),
         ('09', 'Sep'),
        ('10', 'Oct'),
        ('11', 'Nov'),
        ('12', 'Dec'),    
         ],
         string='Fiscal Year', default='6')
    fiscalyear_last_day = fields.Integer(string='Days', default=30)
    
    
    

