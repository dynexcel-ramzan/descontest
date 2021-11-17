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

class ComputationTaxRegister(models.AbstractModel):
    _name = 'report.de_payroll_tax_report.computation_report_pdf'
    _description = 'Computation Tax Register Report'

    '''Find Purchase invoices between the date and find total outstanding amount'''
    @api.model
    def _get_report_values(self,docids, data=None):
        
        docs = self.env['computation.tax.register.wizard'].browse(self.env.context.get('active_id'))
        
        outstanding_invoice = []
        
        invoices = self.env['account.move'].search([('date', '>=', docs.date_from),('date', '<=', docs.date_to)])
        return {
            'docs':docs,
            'invoices': invoices,
        }
        