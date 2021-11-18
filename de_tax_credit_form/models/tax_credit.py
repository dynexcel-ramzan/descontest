from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta


class PayrollReconcile(models.Model):
      _inherit = 'hr.payslip'
      payslip_month = fields.Char(string='Payslip Month',compute='compute_month')
   
      @api.depends('date_from')
      def compute_month(self):
            for pay in self:
                date_from =0
                pay.payslip_month = self.date_from.strftime('%m-%y')