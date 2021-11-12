# -- coding: utf-8 --

from odoo import models, fields, api


class de_payroll_tax_report(models.Model):
    _name = 'de_payroll.tax_report'
    _description = 'de_payroll_tax_report.de_payroll_tax_report'

    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()
    date_of_issue = fields.Date(string="Date of issue")

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100
            
    def print_report(self):
        data={}
        return self.env.ref('de_payroll_tax_report.report_card_xlx').report_action(self, data=data)
    
#      return self.env.ref('excel_reports.report_card_xlx').report_action(self, data=data)
