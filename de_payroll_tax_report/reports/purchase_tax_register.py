# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2019-today Ascetic Business Solution <www.dynexcel.com>

#################################################################################

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError

class PurchaseTaxRegister(models.AbstractModel):
    _name = 'report.de_payroll_tax_report.report_pdf'
    _description = 'Purchase Tax Register Report'

    '''Find Purchase invoices between the date and find total outstanding amount'''
    @api.model
    def _get_report_values(self,docids, data=None):
        incom_tax_vals = []
        docs = self.env['purchase.tax.register.wizard'].browse(self.env.context.get('active_id'))
        
        accounting_entries = self.env['account.move.line'].search([('date', '>=', docs.date_from),('date', '<=', docs.date_to),('partner_id','=', docs.name.address_home_id.id),('debit','!=',0.0)])
        incom_tax_vals = []
        sr_no = 0
        tax_amount = 0 
        for move in accounting_entries:
            payslip = self.env['hr.payslip'].search([('employee_id','=',docs.name.id),('date_from','=', move.date),('date_to','=', move.date)], limit=1)
            for rule in payslip.line_ids:
                if rule.code == 'INC01':
                    tax_amount = rule.amount
            incom_tax_vals.append({
                'date_from': move.date,
#                 'bank_name': move.bank_name,
#                 'branch_address': move.branch_address,
                'tot_net_wage': tax_amount,
            })

        return {
            'docs': docs,
            'accounting_entries': accounting_entries,
            'incom_taxes':incom_tax_vals,
        }
    




       
        
        
