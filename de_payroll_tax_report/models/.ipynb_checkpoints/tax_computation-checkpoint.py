# -- coding: utf-8 --

from odoo import models, fields, api
from datetime import datetime


class PayrollTax(models.Model):
    _name = 'payroll.tax'
#     _description = 'de_payroll_tax_report.de_payroll_tax_report'

    name = fields.Many2one('hr.employee', string="Employee")
    date_from = fields.Date(string="Date from", default=datetime.today())
    date_to = fields.Date(string="Date to", default=datetime.today())
    bank_name = fields.Char(string="Bank Name")
    branch_address = fields.Char(string="Branch address")
    
    
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#     address = fields.Many2one('res.partner', string="Address")
    payslip = fields.Many2one('hr.payslip.line', string="Payslip")


    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
            
    def print_report(self):
        data={}
        return self.env.ref('de_payroll_tax_report.de_payroll_tax_calculation').report_action(self, data=data)
    
#      return self.env.ref('excel_reports.report_card_xlx').report_action(self, data=data)