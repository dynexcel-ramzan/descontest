# -- coding: utf-8 --

# from odoo import models, fields, api
# from datetime import datetime

# from datetime import time
# from datetime import date
# from datetime import timedelta


# class PayrollTax(models.Model):
#     _name = 'payroll.tax'
# #     _description = 'de_payroll_tax_report.de_payroll_tax_report'

#     name = fields.Many2one('hr.employee', string="Employee")
#     date_from = fields.Date(string="Date from", default=datetime.today())
#     date_to = fields.Date(string="Date to", default=datetime.today())
#     bank_name = fields.Char(string="Bank Name")
#     branch_address = fields.Char(string="Branch address")
#     payslip = fields.Many2one('hr.payslip.line', string="Payslip")


#     @api.depends('value')
#     def _value_pc(self):
#             for record in self:
#             record.value2 = float(record.value) / 100
            

#     def print_report(self):
#         moves= self.env['account.move'].search([('partner_id','=',self.name.address_id.id),('date','>=',self.date_from),   ('date','<=',self.date_to)])
        
#         for entry_line in moves:        
#         payslip = self.env['hr.payslip'].search([('name','=',self.name.id),('date_from','>=',self.bank_name),('date_to','<=',self.branch_address)], limit=1)
#                 incom_tex = 0
#                 for rule in payslip.line_ids:
#                     if rule.code =='INC01':
#                         incom_tex = rule.amount
                
#                 final_tax_calc.append({
#                     'date': entry_line.date.strftime('%d-%b-%Y'),
#                     'bank':  self.bank_name,
#                     'address': self.branch_address,
#                     'amount':  incom_tex, 
#                 })
#         data = {'final_tax_calc': final_tax_calc }
#         return self.env.ref('de_payroll_tax_report.de_payroll_tax_calculation').report_action(self, data=data)
    
#      return self.env.ref('excel_reports.report_card_xlx').report_action(self, data=data)