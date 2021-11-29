# -*- coding: utf-8 -*-
# from odoo import http


# class DeEmployeeOvertimeReportDeparmtentWise(http.Controller):
#     @http.route('/de_employee_overtime_report_deparmtent_wise/de_employee_overtime_report_deparmtent_wise/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_employee_overtime_report_deparmtent_wise/de_employee_overtime_report_deparmtent_wise/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_employee_overtime_report_deparmtent_wise.listing', {
#             'root': '/de_employee_overtime_report_deparmtent_wise/de_employee_overtime_report_deparmtent_wise',
#             'objects': http.request.env['de_employee_overtime_report_deparmtent_wise.de_employee_overtime_report_deparmtent_wise'].search([]),
#         })

#     @http.route('/de_employee_overtime_report_deparmtent_wise/de_employee_overtime_report_deparmtent_wise/objects/<model("de_employee_overtime_report_deparmtent_wise.de_employee_overtime_report_deparmtent_wise"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_employee_overtime_report_deparmtent_wise.object', {
#             'object': obj
#         })
