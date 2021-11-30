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


class PayrollReconcile(models.TransientModel):
    _name = 'payroll.reconcile.wizard'
#     _description = 'de_payroll_tax_report.de_payroll_tax_report'

    company_id = fields.Many2one('res.company', string="Name")
    date_from = fields.Date(string="Date from", default=datetime.today())
    date_to = fields.Date(string="Date to", default=datetime.today())
   

    def check_report(self):
        data = {}
        data['form'] = self.read(['date_from', 'date_to'])[0]
        return self.print_report(data)

    def print_report(self,data):
        data['form'].update(self.read(['date_from', 'date_to'])[0])
        return self.env.ref('de_payroll_reconcile_summary_report.open_payroll_reconcile_wizard_action').report_action(self,data=data,config=False)
    
 
