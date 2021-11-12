# -*- coding: utf-8 -*-
# from odoo import http


# class DeLocationwiseOvertimeReport(http.Controller):
#     @http.route('/de_locationwise_overtime_report/de_locationwise_overtime_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_locationwise_overtime_report/de_locationwise_overtime_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_locationwise_overtime_report.listing', {
#             'root': '/de_locationwise_overtime_report/de_locationwise_overtime_report',
#             'objects': http.request.env['de_locationwise_overtime_report.de_locationwise_overtime_report'].search([]),
#         })

#     @http.route('/de_locationwise_overtime_report/de_locationwise_overtime_report/objects/<model("de_locationwise_overtime_report.de_locationwise_overtime_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_locationwise_overtime_report.object', {
#             'object': obj
#         })
