# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class TaxCredit(models.Model):
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
    date = fields.Date(string='Date', required=True)
    tax_amount = fields.Float(string='Amount', required=True)
    reconcile_amount = fields.Float(string='Reconcile Amount' )
    remaining_amount = fields.Float(string='Remaining Amount')
    company_id = fields.Many2one('res.company', string='Company')
    remarks = fields.Char(string='Remarks')
    dist_month = fields.Integer(string='Dist Month', default=1)
    post = fields.Char(string='Post', readonly=True, default='N')
    credit_type_id = fields.Many2one('tax.credit.type', string='Tax Credit Type')
    
    def unlink(self):
        for line in self:
            if line.post != 'N':
                raise UserError(_('You cannot delete an Document  which is Reconciled. '))
     
            return super(TaxCredit, self).unlink()  
    
    @api.onchange('date')
    def onchange_date(self):
        for line in self:
            if line.date:
                line.update({
                    'period': line.date.strftime('%m'),
                    'tax_year': line.date.strftime('%Y'),
                })
                
    
    
    @api.onchange('employee_id')
    def onchange_employee_id(self):
        for line in self:
            if line.employee_id:
                line.update({
                    'name': line.employee_id.name+' ('+line.employee_id.emp_number+')',
                    'company_id': line.employee_id.company_id.id,
                })

