# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeEmailReport(http.Controller):
#     @http.route('/de_employee_email_report/de_employee_email_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_email_report/de_employee_email_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_email_report.listing', {
#             'root': '/de_employee_email_report/de_employee_email_report',
#             'objects': http.request.env['de_employee_email_report.de_employee_email_report'].search([]),
#         })

#     @http.route('/de_employee_email_report/de_employee_email_report/objects/<model("de_employee_email_report.de_employee_email_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_email_report.object', {
#             'object': obj
#         })
