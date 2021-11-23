# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    is_salary_Stop = fields.Boolean(string='Stop Salary')
    current_month_tax_amount = fields.Float(string='Tax Amount')
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
    tax_year = fields.Char(string='Year')
    
    def compute_sheet(self):
        for pay in self:
            pay.update({
                'period':  pay.date_to.strftime('%m'),
                'tax_year': pay.date_to.strftime('%Y'),
            })
        rec = super(HrPayslip, self).compute_sheet()
        for pay in self:
            pay._action_update_income_tax(pay, pay.date_to)
        return rec
    
    
    def _action_update_income_tax(self, payslip, date):
        total_gross_amount = 0
        result = 0
        rule_categ_list = []
        rule_categories=self.env['hr.salary.rule.category'].search([('is_compute_tax','=',True)])
        for rule_categ in rule_categories:
            rule_categ_list.append(rule_categ.id)                
        for rule_line in payslip.line_ids:
            if rule_line.category_id.id in rule_categ_list:
                total_gross_amount +=  rule_line.amount        
        pf=0
        if (payslip.employee_id.pf_member == 'yes_with' or payslip.employee_id.pf_member == 'yes_without' and payslip.company_id.id==6): 
            pf=((payslip.contract_id.wage * 9)/100)*12
        elif (payslip.employee_id.pf_member == 'yes_with' or payslip.employee_id.pf_member == 'yes_without' and payslip.company_id.id!=6): 
            pf=((payslip.contract_id.wage * 6.3)/100)*12
        apf=0
        if(pf>150000):
            apf=pf-150000
        if(apf > 0):
            result= apf 
        initial_fiscal_month = 12 
        stop_salary_fiscal_year=0
        payslips = self.env['hr.payslip'].search([('employee_id','=',payslip.employee_id.id),('tax_year','=',payslip.tax_year),('is_salary_Stop','=',True)])
        for paye in payslips:
            stop_salary_fiscal_year += 1   
        fiscal_month = (initial_fiscal_month - stop_salary_fiscal_year)    
        total_gross =  total_gross_amount + (apf/fiscal_month)   
        if ((total_gross)*fiscal_month>=600001 and (total_gross)*fiscal_month<=1200000):
            result = (round(((((total_gross*fiscal_month)-600000)/100)*5)/12,0))
        elif ((total_gross)*fiscal_month>=1200001 and (total_gross)*fiscal_month<=1800000):
            result = (round((((((categories.GROSS*fiscal_month)-1200000)/100)*10)+30000)/12,0))
        elif ((total_gross)*fiscal_month>=1800001 and (total_gross)*fiscal_month<=2500000):
            result = (round((((((total_gross*fiscal_month)-1800000)/100)*15)+90000)/12,0))
        elif ((total_gross)*fiscal_month>=2500001 and (total_gross)*fiscal_month<=3500000):
            result = (round((((((total_gross*fiscal_month)-2500000)/100)*17.5)+195000)/12,0))
        elif ((total_gross)*fiscal_month>=3500001 and (total_gross)*fiscal_month<=5000000):
            result = (round((((((total_gross*fiscal_month)-3500000)/100)*20)+370000)/12,0))
        elif ((total_gross)*fiscal_month>=5000001 and (total_gross)*fiscal_month<=8000000):
            result = (round((((((total_gross*fiscal_month)-5000000)/100)*22.5)+670000)/12,0))
        elif ((total_gross)*fiscal_month>=8000001 and (total_gross)*fiscal_month<=12000000):
            result = (round((((((total_gross*fiscal_month)-8000000)/100)*25)+1345000)/12,0))
        elif ((total_gross)*fiscal_month>=12000001 and (total_gross)*fiscal_month<=30000000):
            result = (round((((((total_gross*fiscal_month)-12000000)/100)*27.5)+2345000)/12,0))
        elif ((total_gross)*fiscal_month>=30000001 and (total_gross)*fiscal_month<=50000000):
            result = (round((((((total_gross*fiscal_month)-30000000)/100)*30)+7295000)/12,0))
        elif ((total_gross)*fiscal_month>=50000001 and (total_gross)*fiscal_month<=75000000):
            result = (round((((((total_gross*fiscal_month)-50000000)/100)*32.5)+13295000)/12,0))
        elif ((total_gross)*fiscal_month>=75000001):
            result = (round((((((total_gross*fiscal_month)-75000000)/100)*35)+21420000)/12,0))
        else:
            result = 0.0      
        payslip.update({
            'current_month_tax_amount': result,
        })

    
    