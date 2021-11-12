# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta


class PayrollReconcile(models.Model):
      _inherit = 'hr.payslip'
        
      payslip_month = fields.Char(string='Payslip Month',compute='compute_month')
    
      def compute_month(self):
            for pay in self:
                date_from =0
                pay.payslip_month = pay.date_from.strftime('%m-%y')
                
                
            
                    
                    
                    
                    
class SalaryRule(models.Model):
      _inherit = 'hr.salary.rule'
        
      reconcilation_details = fields.Boolean(string="Reconcilation Details")