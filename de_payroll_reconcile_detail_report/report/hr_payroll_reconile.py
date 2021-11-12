# -*- coding: utf-8 -*-

import time
from odoo import api, models, _ , fields 
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo import exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class PayrollReport(models.AbstractModel):
    _name = 'report.de_payroll_reconcile_detail_report.payroll_report'
    _description = 'Payroll Report Report'

    
    
    
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get('active_model')
        docs = self.env['payroll.reconcile.wizard'].browse(self.env.context.get('active_id'))
#         count = 0 
#         compansation_list = []
#         sr_no = 1
#         employees = self.env['hr.employee'].search([('company_id','=',docs.company_id.id)])
#         for emp in employees:
#             previous_month_amount = next_month_amount = 0
#             rec_date = docs.date_from
#             delta_days = ((docs.date_to - docs.date_from).days)/30
#             for month in range (round(delta_days)):
#                 employee_count = net_amount = ovt_amount = basic_salary = net_description = 0
#                 rec_date = rec_date + timedelta(month)
#                 monthly_payslip = self.env['hr.payslip'].search([('employee_id','=',emp.id),('date_from','<=', rec_date),('date_to','>=', rec_date)]) 
#                 for payslip in monthly_payslip:
#                     for rule in payslip.line_ids:
#                         if rule.code == 'PF02':
#                             if count >= 1:
#                                 next_month_amount = rule.amount
#                             else:
#                                 previous_month_amount = rule.amount
#                 count += 1 

#             compansation_list.append({
#                 'sr_no': sr_no,
#                 'number': emp.emp_number,
#                 'employee': emp.name,
#                 'previous_month_amount': previous_month_amount,
#                 'next_month_amount': next_month_amount,
#             })   
#             sr_no += 1
            
#         compansation_list.append({
#                 'sr_no': sr_no,
#                 'number': ' ',
#                 'employee': 'Basic Salary',
#                 'previous_month_amount': 1,
#                 'next_month_amount': 2,
#             })       
#         employees = self.env['hr.employee'].search([('company_id','=',docs.company_id.id)])
#         for emp in employees:
#             previous_month_amount = next_month_amount = 0
#             rec_date = docs.date_from
#             delta_days = ((docs.date_to - docs.date_from).days)/30
#             for month in range (round(delta_days)):
#                 employee_count = net_amount = ovt_amount = basic_salary = net_description = 0
#                 rec_date = rec_date + timedelta(month)
#                 monthly_payslip = self.env['hr.payslip'].search([('employee_id','=',emp.id),('date_from','<=', rec_date),('date_to','>=', rec_date)]) 
#                 for payslip in monthly_payslip:
#                     for rule in payslip.line_ids:
#                         if rule.code == 'BASIC':
#                             if count >= 1:
#                                 next_month_amount = rule.amount
#                             else:
#                                 previous_month_amount = rule.amount
#                 count += 1 

#             compansation_list.append({
#                 'sr_no': sr_no,
#                 'number': emp.emp_number,
#                 'employee': emp.name,
#                 'previous_month_amount': previous_month_amount,
#                 'next_month_amount': next_month_amount,
#             })   
#             sr_no += 1     

                                    
        return {
            'docs': docs,
#             'compansation_list': compansation_list
        }