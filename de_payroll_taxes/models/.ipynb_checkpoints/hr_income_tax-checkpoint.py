# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrIncomeTax(models.Model):
    _name = 'hr.income.tax'
    _description = 'HR Income Tax'
    
    name = fields.Char(string='Name', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    period = fields.Selection( 
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
         string='Period')
    tax_year = fields.Char(string='Tax Year')
    date = fields.Date(string='Date')
    tax_amount = fields.Float(string='Amount', required=True)
    company_id = fields.Many2one('res.company', string='Company')
    
    
    def _action_update_income_tax(self, payslip, date):
        total_gross_amount = 0
        rule_categ_list = []
        rule_categories=self.env['hr.salary.rule.category'].search([('is_compute_tax','=',True)])
            for rule_categ in rule_categories:
                rule_categ_list.append(rule_categ.id)
                
        for rule_line in payslip.line_ids:
            if rule_line.category_id.id in rule_categ_list:
                total_gross_amount +=  rule_line.amount   
        date_period = date.strftime('%m')
        date_year = date.strftime('%Y')
        current_income_tax=self.env['hr.income.tax'].search([('employee_id','=',employee),('tax_year','=',date_year),('period','=',date_period)], limit=1)
        tax_amount = 0
        current_income_tax.update({
            'tax_amount': tax_amount,
        })
        
    
    
    def _action_create_income_tax(self):
        companies = self.env['res.company'].search([])
        for company in companies:
            employees=self.env['hr.employee'].search([('company_id','=',company.id)])
            for emp in employees:
                month_range = 12
                for tax_rec in range(month_range):
                    ext_income_tax = self.env['hr.income.tax'].search([('employee_id','=',emp.id),('tax_year','=',fields.date.today().strftime('%y')),('period','=',str(tax_rec+1))])
                    if not ext_income_tax:
                        tax_vals = {
                            'name': emp.name +' ('+str(emp.emp_number)+') ',
                            'employee_id': emp.id,
                            'period':  str(tax_rec+1),
                            'tax_year': fields.date.today().strftime('%Y'),
                            'tax_amount': 0,
                            'date': fields.date.today(),
                            'company_id': emp.company_id.id,
                        }
                        tax_values = self.env['hr.income.tax'].create(tax_vals)

    
    
    

