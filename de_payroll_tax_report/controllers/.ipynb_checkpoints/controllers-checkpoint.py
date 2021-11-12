# -*- coding: utf-8 -*-
# from odoo import http


# class DePayrollTaxReport(http.Controller):
#     @http.route('/de_payroll_tax_report/de_payroll_tax_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_payroll_tax_report/de_payroll_tax_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_payroll_tax_report.listing', {
#             'root': '/de_payroll_tax_report/de_payroll_tax_report',
#             'objects': http.request.env['de_payroll_tax_report.de_payroll_tax_report'].search([]),
#         })

#     @http.route('/de_payroll_tax_report/de_payroll_tax_report/objects/<model("de_payroll_tax_report.de_payroll_tax_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_payroll_tax_report.object', {
#             'object': obj
#         })
