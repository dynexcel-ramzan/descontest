# -- coding: utf-8 --
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#################################################################################
import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta

class ComputationTaxRegister(models.AbstractModel):
        _name = 'report.de_payroll_reconcile_summary_report.computation_rep'
        _description = 'Computation Tax Register Report'

        '''Find payslip between the date and find total amount'''

        @api.model
        def _get_report_values(self, docids, data=None):
                docs = self.env['payroll.reconcile.wizard'].browse(self.env.context.get('active_id'))               
                reconcile_list = []
                compansation_list = []
                deduction_list = []
                previous_payslips = self.env['hr.payslip'].search([('company_id','=',docs.company_id.ids),('date_from','>=',docs.date_from),('date_to','<=',docs.date_from)]) 
                curr_payslips = self.env['hr.payslip'].search([('company_id','=',docs.company_id.ids),('date_from','>=',docs.date_to),('date_to','<=',docs.date_to)])
                prev_month_net_amount = curr_month_net_amount = employee_count = 0
                for pre_slip in previous_payslips:
                    for pre_rule in pre_slip.line_ids:
                        if pre_rule.code == 'NET':
                            prev_month_net_amount += pre_rule.amount  
                for curr_slip in curr_payslips:
                    for curr_rule in curr_slip.line_ids:
                        if curr_rule.code == 'NET':
                            curr_month_net_amount += curr_rule.amount  
                if prev_month_net_amount > 0:
                    reconcile_list.append({
                        'desc': 'Net Salary of '+str(employee_count)+' employee For '+str(docs.date_from.strftime('%b-%Y')),     
                        'amount': prev_month_net_amount,
                    })
                if curr_month_net_amount > 0:
                    reconcile_list.append({
                        'desc': 'Net Salary of '+str(employee_count)+' employee For '+str(docs.date_to.strftime('%b-%Y')),     
                        'amount': curr_month_net_amount,
                    })    
                compansation_rule = self.env['hr.salary.rule'].search([('reconcilation_compensation','=','True'),
                                                                     ('reconcilation_deduction','=','True'), ])
                for comp in compansation_rule: 
                    comp_pre_month_amount = comp_curr_month_amount = 0
                    for pre_slip in previous_payslips:
                        for pre_rule in pre_slip.line_ids:
                            if pre_rule.code == comp.code:
                                prev_month_net_amount += pre_rule.amount  
                    for curr_slip in curr_payslips:
                        for curr_rule in curr_slip.line_ids:
                            if curr_rule.code == comp.code:
                                curr_month_net_amount += curr_rule.amount
                    compansation_list.append({
                        'rule_name': comp.name,
                        'comp_pre_month_amount': comp_pre_month_amount,
                        'comp_curr_month_amount' : comp_curr_month_amount,
                        'arrears' : 0,
                    })
                deduction_rule = self.env['hr.salary.rule'].search([('category_id.code','=','DED')])
                for ded in deduction_rule:
                    ded_pre_month_amount = ded_curr_month_amount = 0
                    for ded_prev_slip in previous_payslips:
                        for ded_prev_rule in ded_prev_slip.line_ids:
                            if ded_prev_rule.code == comp.code:
                                prev_month_net_amount += ded_prev_rule.amount  
                    for ded_curr_slip in curr_payslips:
                        for ded_curr_rule in ded_curr_slip.line_ids:
                            if ded_curr_rule.code == comp.code:
                                curr_month_net_amount += ded_curr_rule.amount
                    deduction_list.append({
                        'rule_name': ded.name,
                        'ded_pre_month_amount': ded_pre_month_amount,
                        'ded_curr_month_amount' : ded_curr_month_amount,
                        'arrears' : 0,
                    })    
                    
                return {
                    'docs': docs,
                    'reconcile_list': reconcile_list,
                    'compansation_list': compansation_list,
                    'deduction_list': deduction_list,
                }
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
                                                           
#                                                              ('date_from', '>=', docs.date_from), ('date_to', '<=', docs.date_to)

#  'car_allowance': car_allowance,
#                                 'bonus': bonus,
#                                 'arrears': arrears,
#                                 'overtime': overtime,
#                                 'mobile_allowance': mobile_allowance,
#                                 'tot_net_wage': tax_amount,
#                                 'tot_bonus_amount': bonus_amount,
#                                 'tot_car_allow': tot_car_allow,
#                                 'tot_arrears': tot_arrears,
#                                 'tot_overtime': tot_overtime,
#                                 'tot_incentive': tot_incentive,
#                                 'tot_mobile_allow': tot_mobile_allow,
#                                 'incom_tax': incom_tax,
#                                 'tot_incom_tax': tot_incom_tax,
#                                 'net_sallary': net_sallary,
#                                 'base_sallary': base_sallary,
#                                 'accomodation': accomodation,

#   tot_ot_amount = rule.amount
#                                 tot_gross_pay = rule.amount
#                                 tax_amount = rule.amount
#                                 bonus_amount = rule.amount
#                                 tot_car_allow = rule.amount
#                                 tot_arrears = rule.amount
#                                 tot_overtime = rule.amount
#                                 tot_others = rule.amount
#                                 tot_incentive = rule.amount
#                                 tot_mobile_allow = rule.amount
#                                 incom_tax = rule.amount
#                                 tot_incom_tax = rule.amount



#   for payslip in monthly_payslips:
#                         employee_count += 1
#                         for rule in payslip.line_ids:
#                             if rule.category_id.code=='COMP':
#                                 if rule.code == 'OT100':
#                                     ovt_amount = rule.amount
#                                 if rule.code == 'BASIC':
#                                     basic_salary = rule.amount

#                             if rule.category_id.code=='DED':
#                                 pass

#                             if rule.category_id.code=='NET': 
# #                                 if rule.code='NET':
#                                     net_amount += rule.amount



#                                 if count >= 1:
#                                     next_month_amount += rule.amount
#                                 else:
#                                     previous_month_amount += rule.amount



#                 for month in range (round(delta_days)):
#                     employee_count = next_month_amount = net_amount = previous_month_amount = basic_salary = net_description = 0
#                     employee_count += 1
                            




        