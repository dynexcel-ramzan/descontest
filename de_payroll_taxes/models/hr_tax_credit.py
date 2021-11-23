# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class de_payroll_taxes(models.Model):
    _name = 'hr.tax.credit'
    _description = 'HR Tax Credit'
    
    
    name = fields.Char(string='Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    period = fields.Selection( 
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
         string='Period')
    tax_year = fields.Char(string='Tax Year')
    date = fields.Date(string='Date')
    tax_amount = fields.Float(string='Amount', required=True)
    company_id = fields.Many2one('res.company', string='Company')
    
    
    

