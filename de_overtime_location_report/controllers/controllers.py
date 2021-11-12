# -*- coding: utf-8 -*-
# from odoo import http


# class DeOvertimeLocationReport(http.Controller):
#     @http.route('/de_overtime_location_report/de_overtime_location_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_overtime_location_report/de_overtime_location_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_overtime_location_report.listing', {
#             'root': '/de_overtime_location_report/de_overtime_location_report',
#             'objects': http.request.env['de_overtime_location_report.de_overtime_location_report'].search([]),
#         })

#     @http.route('/de_overtime_location_report/de_overtime_location_report/objects/<model("de_overtime_location_report.de_overtime_location_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_overtime_location_report.object', {
#             'object': obj
#         })
