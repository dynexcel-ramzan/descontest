# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeEobiReport(http.Controller):
#     @http.route('/de_employee_eobi_report/de_employee_eobi_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_eobi_report/de_employee_eobi_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_eobi_report.listing', {
#             'root': '/de_employee_eobi_report/de_employee_eobi_report',
#             'objects': http.request.env['de_employee_eobi_report.de_employee_eobi_report'].search([]),
#         })

#     @http.route('/de_employee_eobi_report/de_employee_eobi_report/objects/<model("de_employee_eobi_report.de_employee_eobi_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_eobi_report.object', {
#             'object': obj
#         })
