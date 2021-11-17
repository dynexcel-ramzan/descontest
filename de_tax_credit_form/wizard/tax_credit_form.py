# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#
#################################################################################

from odoo import models, fields, api
from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta


class TaxCredit(models.TransientModel):
    _name = 'tax.credit'
    _description = 'Tax Credit form fo calculations'
        
    investment_amount = fields.Float(string= "Investment Amount")
    
                        

                        if rule.code == 'INC01':
                            incom_tax = rule.amount
    
    
     def tax_credit(self):
            
            tot_tax_income = self.env['hr.payslip'].search([])
            for rule in multiple_slips.line_ids:
            
#                 ('shipment_service_id', '=', self.id)
            
            
                        incom_tax = 0

        # expected bills
        amount = sum(delivered_service.mapped('sale'))
        payable = sum(delivered_service.mapped('cost'))
        self.exp_receivable = amount
        self.exp_payable = payable
        margin = self.exp_receivable - self.exp_payable
        self.exp_margin = margin
        # expected bills ends
        # Actual Payment start
        # actual payable
        to_pay = sum(exp_payable.mapped('amount_total'))
        get_residual = sum(exp_payable.mapped('amount_residual'))
        actual_to_pay = to_pay - get_residual
        self.actual_payable = actual_to_pay
        # actual receivable
        to_recceive = sum(exp_receivable.mapped('amount_total'))
        rec_residual = sum(exp_receivable.mapped('amount_residual'))
        actual_to_receive = to_recceive - rec_residual
        self.actual_receivable = actual_to_receive
        # actual margin
        self.actual_margin = self.actual_receivable - self.actual_payable
        # ask sir
        # actual payment ends
        # Due amount
        self.receivable_due = rec_residual
        self.payable_due = get_residual
    

    

    def check_report(self):
        data = {}
        data['form'] = self.read()[0]
        return self.print_report(data)

    def print_report(self, data):
        data['form'].update(self.read()[0])
        return self.env.ref('de_tax_credit_form.open_computation_tax_register_action').report_action(self, data=data,
                                                                                                 config=False)
