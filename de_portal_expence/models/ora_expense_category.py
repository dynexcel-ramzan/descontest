# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class OraExpenseCategory(models.Model):
    _name = 'ora.expense.category'
    _description = 'ORA Expense Category'
    
    name = fields.Char(string='Name', required=True)
    company_id  = fields.Many2one('res.company', string='Company')

