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

class ComputationTaxRegister(models.AbstractModel):
        _name = 'report.de_computation_tax_report.computation_report_pdf'
        _description = 'Computation Tax Register Report'

        '''Find Purchase payslip between the date and find total outstanding amount'''

        @api.model
        def _get_report_values(self, docids, data=None):
                docs = self.env['computation.tax.register.wizard'].browse(self.env.context.get('active_id'))
                
                payslip_fild = self.env['computation.tax'].search([])
                
                payslip = []

                accounting_computation = self.env['account.move.line'].search(
                    [('date', '>=', docs.date_from), ('date', '<=', docs.date_to),
                     ('partner_id', '=', docs.employee_id.address_home_id.id)])

                compute_tax_vals = []
                tax_amount = 0
                tot_ot_amount = 0
                tot_gross_pay = 0
                bonus_amount = 0
                tot_car_allow = 0
                tot_arrears = 0
                tot_overtime = 0
                tot_others = 0
                tot_incentive = 0
                tot_mobile_allow = 0
                incom_tax = 0
                tot_incom_tax = 0
                  

                payslip = self.env['hr.payslip'].search([('employee_id', '=', docs.employee_id.id),
                                                          ('date_from', '>=', docs.date_from), ('date_to', '<=', docs.date_to)])
                for multiple_slips in payslip:

                    for rule in multiple_slips.line_ids:
                        incom_tax = ot_amount = car_allowance = bonus = arrears = overtime = others = incentive = mobile_allowance = gross_pay = 0

                        if rule.code == 'INC01':
                            incom_tax = rule.amount
                        elif  rule.code == 'OT100':  
                            ot_amount = rule.amount 
                        elif rule.code == 'CAR01':
                            car_allowance = rule.amount
                        elif rule.code == 'B01':
                            bonus = rule.amount
                        elif rule.code == 'ARR01':
                            arrears = rule.amount
                        elif rule.code == 'OVR01':
                            overtime = rule.amount
                        elif rule.code == 'OR01':
                            others = rule.amount
                        elif rule.code == 'IN01':
                            incentive = rule.amount
                        elif rule.code == 'MOB01':
                            mobile_allowance = rule.amount
                        elif rule.code == 'GROSS':
                            gross_pay = rule.amount
                            
                            tot_ot_amount = rule.amount
                            tot_gross_pay = rule.amount
                            tax_amount = rule.amount
                            bonus_amount = rule.amount
                            tot_car_allow = rule.amount
                            tot_arrears = rule.amount
                            tot_overtime = rule.amount
                            tot_others = rule.amount
                            tot_incentive = rule.amount
                            tot_mobile_allow = rule.amount
                            incom_tax = rule.amount
                            tot_incom_tax = rule.amount
                             

                        compute_tax_vals.append({
                            'date_from': multiple_slips.date,
                            'employee_id': multiple_slips.employee_id,
                            'gross_pay': gross_pay,
                            'tot_gross_pay': tot_gross_pay,
                            'tot_ot_amount': tot_ot_amount,
                            'ot_amount': ot_amount,
                            'car_allowance': car_allowance,
                            'bonus': bonus,
                            'arrears': arrears,
                            'overtime': overtime,
                            'others': others,
                            'incentive': incentive,
                            'mobile_allowance': mobile_allowance,
                            'tot_net_wage': tax_amount,
                            'tot_bonus_amount': bonus_amount,
                            'tot_car_allow': tot_car_allow,
                            'tot_arrears': tot_arrears,
                            'tot_overtime': tot_overtime,
                            'tot_others': tot_others,
                            'tot_incentive': tot_incentive,
                            'tot_mobile_allow': tot_mobile_allow,
                            'incom_tax': incom_tax,
                            'tot_incom_tax': tot_incom_tax,
                            
                        })
                return {
                    'payslip_fild': payslip_fild,
                    'docs': docs,
                    'payslip': compute_tax_vals,
                }
        