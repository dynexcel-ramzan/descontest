# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]

class OraExpenseCategory(models.Model):
    _name = 'ora.expense.category'
    _description = 'ORA Expense Category'
    
    name = fields.Char(string='Name', required=True)
    company_id  = fields.Many2one('res.company', string='Company')
    has_vehicle = fields.Selection(CATEGORY_SELECTION, string="Vehicle Name", default="no", required=True)
    has_reading = fields.Selection(CATEGORY_SELECTION, string="Vehicle Reading", default="no", required=True)

    
    